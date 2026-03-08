import os
import requests

def get_ra_data():
    user = os.getenv('RA_USER')
    key = os.getenv('RA_KEY')
    url = f"https://retroachievements.org/API/API_GetUserRecentlyPlayedGames.php?z={user}&y={key}&u={user}&count=5"
    
    response = requests.get(url)
    if response.status_status == 200:
        data = response.json()
        lines = ["\n### 🎮 Recentemente jogado no RetroAchievements:\n"]
        for game in data:
            lines.append(f"- **{game['Title']}** ({game['ConsoleName']}) - {game['NumAchieved']}/{game['NumPossibleAchievements']} conquistas\n")
        return "".join(lines)
    return ""

def update_readme(new_content):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = ""
    end_marker = ""
    
    start_index = content.find(start_marker) + len(start_marker)
    end_index = content.find(end_marker)
    
    new_readme = content[:start_index] + new_content + content[end_index:]
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

if __name__ == "__main__":
    stats = get_ra_data()
    if stats:
        update_readme(stats)
