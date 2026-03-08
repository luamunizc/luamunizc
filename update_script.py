import os
import requests

def get_ra_data():
    user = os.getenv('RA_USER')
    key = os.getenv('RA_KEY')
    url = f"https://retroachievements.org/API/API_GetUserRecentlyPlayedGames.php?z={user}&y={key}&u={user}&count=5"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if not data or not isinstance(data, list):
                return "\nNenhuma atividade recente encontrada.\n"
                
            lines = ["\n### 🎮 Recentemente jogado no RetroAchievements:\n"]
            for game in data:
                title = game.get('Title', 'Jogo Desconhecido')
                console = game.get('ConsoleName', 'Retro')
                achieved = game.get('NumAchieved', 0)
                possible = game.get('NumPossibleAchievements', 0)
                lines.append(f"- **{title}** ({console}) - {achieved}/{possible} conquistas\n")
            return "".join(lines)
    except Exception as e:
        print(f"Erro: {e}")
    return ""

def update_readme(new_content):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = ""
    end_marker = ""
    
    if start_marker not in content or end_marker not in content:
        print("ERRO: As tags não foram encontradas no README!")
        return

    parts_before = content.split(start_marker)
    parts_after = parts_before[1].split(end_marker)
    
    final_content = parts_before[0] + start_marker + new_content + end_marker + parts_after[1]
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(final_content)

if __name__ == "__main__":
    stats = get_ra_data()
    if stats:
        update_readme(stats)
