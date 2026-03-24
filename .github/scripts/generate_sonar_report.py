import os
import json
import urllib.request
import urllib.error
import urllib.parse
import base64

def get_sonar_prop(key):
    try:
        with open('sonar-project.properties', 'r') as f:
            for line in f:
                if line.startswith(key + '='):
                    return line.split('=')[1].strip()
    except FileNotFoundError:
        print("sonar-project.properties not found.")
    return None

def main():
    sonar_token = os.getenv('SONAR_TOKEN')
    if not sonar_token:
        print("SONAR_TOKEN environment variable is not set.")
        return

    project_key = get_sonar_prop('sonar.projectKey')
    if not project_key:
        print("Could not find sonar.projectKey in sonar-project.properties.")
        return

    github_event_name = os.getenv('GITHUB_EVENT_NAME')
    github_ref_name = os.getenv('GITHUB_REF_NAME')
    github_event_path = os.getenv('GITHUB_EVENT_PATH')

    params = {'component': project_key}

    # Determine Branch or PR
    if github_event_name == 'pull_request' and github_event_path:
        try:
            with open(github_event_path, 'r') as f:
                event_data = json.load(f)
                pr_number = event_data.get('pull_request', {}).get('number')
                if pr_number:
                    params['pullRequest'] = str(pr_number)
                else:
                    print("Could not extract PR number from event path.")
        except Exception as e:
            print(f"Error reading event path: {e}")
    else:
        # Standard branch push
        if github_ref_name:
            # github_ref_name might be 'main' or 'feat/something'
            # For SonarCloud, we usually just pass the branch name
            params['branch'] = github_ref_name

    # Metrics to fetch
    metrics = "alert_status,bugs,vulnerabilities,code_smells,coverage,sqale_index,sqale_rating"
    params['metricKeys'] = metrics

    query_string = urllib.parse.urlencode(params)
    url = f"https://sonarcloud.io/api/measures/component?{query_string}"

    # Basic Auth setup
    auth_str = f"{sonar_token}:"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_b64}'
    }

    print(f"Fetching metrics from: {url}")
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        # Print response body if available for debugging
        try:
            print(e.read().decode())
        except:
            pass
        return
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return

    # Save raw JSON
    with open('sonar-report.json', 'w') as f:
        json.dump(data, f, indent=2)

    # Parse Measures
    measures = {}
    component_data = data.get('component', {})
    for measure in component_data.get('measures', []):
        measures[measure['metric']] = measure['value']

    status = measures.get('alert_status', 'N/A')
    bugs = measures.get('bugs', '0')
    vulnerabilities = measures.get('vulnerabilities', '0')
    code_smells = measures.get('code_smells', '0')
    coverage = measures.get('coverage', '—')
    
    status_icon = "✅" if status == "OK" else "❌" if status == "ERROR" else "⚠️"

    dashboard_url = f"https://sonarcloud.io/dashboard?id={project_key}"
    if 'branch' in params:
         dashboard_url += f"&branch={params['branch']}"
    elif 'pullRequest' in params:
         dashboard_url += f"&pullRequest={params['pullRequest']}"

    # Build Markdown
    markdown = f"""# 📊 Rapport SonarQube

| Métrique | Valeur | Statut |
| :--- | :--- | :--- |
| **Quality Gate** | **{status}** | {status_icon} |
| 🐛 Bugs | {bugs} | |
| 🛡️ Vulnérabilités | {vulnerabilities} | |
| 🧹 Code Smells | {code_smells} | |
| 📈 Couverture | {coverage}% | |

---

🔗 **[Voir le tableau de bord complet]({dashboard_url})**
"""

    # Save Markdown
    with open('sonar-report.md', 'w') as f:
        f.write(markdown)

    print("SonarQube reports generated: sonar-report.json, sonar-report.md")

    # Add to GitHub Step Summary if running in action
    summary_file = os.getenv('GITHUB_STEP_SUMMARY')
    if summary_file:
        try:
            with open(summary_file, 'a') as f:
                f.write("\n" + markdown)
            print("Added to GitHub Step Summary.")
        except Exception as e:
             print(f"Failed to write to GITHUB_STEP_SUMMARY: {e}")

if __name__ == "__main__":
    main()
