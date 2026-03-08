import os
import requests

def get_ra_data():
    user = os.getenv('RA_USER')
    key = os.getenv('RA_KEY')
    # Endpoint corrigido e verificação de status
    url = f"https://retroachievements.org/API/API_GetUserRecentlyPlayedGames.php?z={user}&y={key}&u={user}&count=5"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if not data:
                return "Nenhum jogo jogado recentemente."
                
            lines = ["\n### 🎮 Recentemente jogado no RetroAchievements:\n"]
            for game in data:
                # O RA às semelhanças de chaves pode variar, garantindo que existem
                title = game.get('Title', 'Desconhecido')
                console = game.get('ConsoleName', 'Retro')
                achieved = game.get('NumAchieved', 0)
                possible = game.get('NumPossibleAchievements', 0)
                lines.append(f"- **{title}** ({console}) - {achieved}/{possible} conquistas\n")
            return "".join(lines)
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
    return ""

def update_readme(new_content):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = ""
    end_marker = ""
    
    if start_marker not in content or end_marker not in content:
        print("Marcadores não encontrados no README.md")
        return

    start_index = content.find(start_marker) + len(start_marker)
    end_index = content.find(end_marker)
    
    new_readme = content[:start_index] + new_content + content[end_index:]
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

if __name__ == "__main__":
    stats = get_ra_data()
    if stats:
        update_readme(stats)
        print("README atualizado com sucesso!")
