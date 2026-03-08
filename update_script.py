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
        print(f"Erro na API: {e}")
    return ""

def update_readme(new_content):
    start_tag = ""
    end_tag = ""
    
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    if start_tag not in content or end_tag not in content:
        print("ERRO: Tags não encontradas no README.md!")
        return

    try:
        before_part = content.split(start_tag)[0]
        after_part = content.split(end_tag)[1]
        
        final_readme = f"{before_part}{start_tag}{new_content}{end_tag}{after_part}"
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(final_readme)
        print("README atualizado com sucesso no local correto!")
    except Exception as e:
        print(f"Erro ao processar strings: {e}")

if __name__ == "__main__":
    stats = get_ra_data()
    if stats:
        update_readme(stats)
