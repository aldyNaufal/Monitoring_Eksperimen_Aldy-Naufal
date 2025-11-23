import time
import requests
import random

URL = "http://localhost:8000/predict"

SAMPLES = [
    # === MOBA ===
    {"title": "Push rank Mobile Legends bareng teman", "description": "Mencapai mythic dengan hero assassin di server Indonesia", "tags": "mlbb mobile legends moba rank"},
    {"title": "Solo queue MLBB tanpa tank", "description": "Main hyper carry di rank legend", "tags": "mlbb solo rank moba"},
    {"title": "Custom 5 vs 5 turnamen MLBB", "description": "Scrim melawan tim lokal", "tags": "mobile legends scrim tournament moba"},
    {"title": "Road to Mythical Glory", "description": "Spam hero marksman jagoanku", "tags": "mlbb marksman moba"},
    {"title": "Top global hero Fanny gameplay", "description": "Montage kabel Fanny full damage", "tags": "mlbb fanny montage moba"},
    {"title": "Dota 2 comeback dari mega creep", "description": "Base defense epik di late game", "tags": "dota2 moba comeback"},
    {"title": "Dota 2 ranked spam mid hero", "description": "Main Storm Spirit di high MMR", "tags": "dota2 midlane moba"},
    {"title": "League of Legends pentakill montage", "description": "Menggunakan Yasuo di ranked", "tags": "league of legends lol moba"},
    {"title": "ARAM fun game bareng teman LOL", "description": "Santai main di Howling Abyss", "tags": "lol aram casual moba"},
    {"title": "Wild Rift rank climb di Emerald", "description": "Main Baron lane dengan hero tank", "tags": "wild rift moba mobile"},
    {"title": "Arena of Valor ranked gameplay", "description": "Mencoba hero baru di patch terbaru", "tags": "aov arena of valor moba"},

    # === FPS ===
    {"title": "Valorant clutch 1v5 di overtime", "description": "Clutch menggunakan Jett di Ascent", "tags": "valorant fps shooter clutch"},
    {"title": "Training aim Valorant di range", "description": "Latihan flick dan tracking", "tags": "valorant aim training fps"},
    {"title": "CS2 competitive match Mirage", "description": "Full tryhard sebagai AWPer", "tags": "cs2 counter strike fps"},
    {"title": "CSGO nostalgia highlight", "description": "Kompilasi frag lama di Mirage dan Dust2", "tags": "csgo highlight fps"},
    {"title": "Overwatch 2 ranked sebagai support", "description": "Main Ana dan Kiriko di ladder", "tags": "overwatch2 fps hero shooter"},
    {"title": "Apex Legends frag movie", "description": "High kill game di World's Edge", "tags": "apex legends fps battle royale"},
    {"title": "Rainbow Six Siege tactical push", "description": "Menyerbu site dengan koordinasi tim", "tags": "r6 siege fps tactical"},
    {"title": "Call of Duty MW2 multiplayer chaos", "description": "Gameplay TDM dengan senjata SMG", "tags": "cod mw2 fps"},
    {"title": "Valorant deathmatch aim warmup", "description": "Persiapan sebelum ranked", "tags": "valorant warmup fps"},
    {"title": "Valorant montage headshot clean", "description": "Kompilasi one tap sheriff", "tags": "valorant montage fps"},

    # === Battle Royale ===
    {"title": "PUBG Mobile chicken dinner solo vs squad", "description": "Menang di Erangel dengan 18 kill", "tags": "pubgm pubg battle royale mobile"},
    {"title": "PUBG PC late circle intense fight", "description": "Clutch terakhir melawan dua squad", "tags": "pubg pc battle royale"},
    {"title": "Fortnite build battle high ground", "description": "Edit cepat melawan pemain pro", "tags": "fortnite battle royale building"},
    {"title": "Apex Legends ranked predator push", "description": "Trio ranked dengan Wraith, Pathfinder, dan Bangalore", "tags": "apex legends ranked battle royale"},
    {"title": "Free Fire ranked master gameplay", "description": "Push rank dengan squad random", "tags": "free fire battle royale"},
    {"title": "Warzone 2 victory clutch", "description": "Sisa satu squad lawan di gulag dan zona akhir", "tags": "warzone battle royale"},
    {"title": "PUBG Mobile TDM training aim", "description": "Latihan recoil control senjata AR", "tags": "pubgm tdm training"},
    {"title": "Fortnite no build mode win", "description": "Gameplay tanpa building fokus aim", "tags": "fortnite nobuild battle royale"},
    {"title": "Apex Legends solo queue chaos", "description": "Main sendirian di ranked", "tags": "apex solo battle royale"},
    {"title": "PUBG Mobile fun custom room", "description": "Custom game bareng komunitas", "tags": "pubgm custom battle royale"},

    # === RPG / JRPG ===
    {"title": "Genshin Impact Spiral Abyss clear", "description": "12-3 full star dengan tim meta", "tags": "genshin rpg spiral abyss"},
    {"title": "Exploration di Sumeru Genshin", "description": "Mencari chest dan puzzle dendro", "tags": "genshin open world rpg"},
    {"title": "Honkai Star Rail boss fight", "description": "Melawan boss endgame tingkat tinggi", "tags": "hsr honkai star rail rpg"},
    {"title": "Elden Ring malenia boss no hit", "description": "Penantang tersulit di Elden Ring", "tags": "elden ring soulslike rpg"},
    {"title": "Final Fantasy VII Remake combat showcase", "description": "Bertarung sebagai Cloud dan Tifa", "tags": "ff7 remake jrpg rpg"},
    {"title": "Persona 5 Royal daily life sim", "description": "Mengatur jadwal sekolah dan dungeon", "tags": "persona5 jrpg rpg"},
    {"title": "Xenoblade Chronicles exploration", "description": "Menjelajah area luas dan grinding", "tags": "xenoblade rpg"},
    {"title": "Diablo IV endgame build showcase", "description": "Dungeon run dengan build barbarian", "tags": "diablo arpg rpg"},
    {"title": "Genshin Impact daily commissions", "description": "Rutinitas harian pemain F2P", "tags": "genshin daily rpg"},
    {"title": "Skyrim modded adventure", "description": "Menggunakan banyak mod grafis", "tags": "skyrim mod rpg open world"},

    # === Simulation / Management ===
    {"title": "Cities Skylines membuat kota anti macet", "description": "Mendesain jalan tol dan interchange", "tags": "cities skylines city builder simulation"},
    {"title": "Transport Fever 2 train network", "description": "Membuat jalur kereta efisien", "tags": "transport fever simulation"},
    {"title": "The Sims 4 keluarga chaos", "description": "Drama rumah tangga sim lucu", "tags": "sims4 life simulation"},
    {"title": "House Flipper renovation", "description": "Renov rumah kecil jadi mewah", "tags": "house flipper simulation"},
    {"title": "Farming Simulator 22 panen besar", "description": "Mengelola ladang gandum dan jagung", "tags": "farming simulator agriculture"},
    {"title": "PC Building Simulator rakit PC", "description": "Merakit PC budget gaming", "tags": "pc building simulator"},
    {"title": "PowerWash Simulator bersihin halaman", "description": "Membersihkan kotoran pakai powerwash", "tags": "powerwash sim relaxing"},
    {"title": "Football Manager 2024 taktikal match", "description": "Mengatur taktik klub besar Eropa", "tags": "fm24 football manager simulation"},
    {"title": "Euro Truck Simulator 2 long haul", "description": "Mengantar kargo jarak jauh malam hari", "tags": "ets2 truck simulator driving"},
    {"title": "Bus Simulator Indonesia rute kota", "description": "Mengantar penumpang keliling kota", "tags": "bussid bus simulator indonesia"},

    # === Sandbox / Creative ===
    {"title": "Minecraft survival hardcore no death", "description": "Hari pertama bertahan hidup", "tags": "minecraft hardcore survival sandbox"},
    {"title": "Minecraft building modern house", "description": "Membangun rumah minimalis keren", "tags": "minecraft build creative"},
    {"title": "Roblox roleplay game", "description": "Bermain peran di kota virtual", "tags": "roblox roleplay sandbox"},
    {"title": "Roblox obby parkour sulit", "description": "Mencoba obstacle course tersulit", "tags": "roblox obby parkour"},
    {"title": "Terraria expert mode boss rush", "description": "Melawan semua boss di satu dunia", "tags": "terraria sandbox adventure"},
    {"title": "Garry's Mod sandbox chaos", "description": "Eksperimen dengan berbagai addon", "tags": "gmod sandbox"},
    {"title": "Brick Rigs crash compilation", "description": "Tabrakan kendaraan lucu", "tags": "brick rigs sandbox"},
    {"title": "Scrap Mechanic build kendaraan unik", "description": "Menciptakan mobil dan mesin aneh", "tags": "scrap mechanic sandbox"},
    {"title": "Minecraft redstone tutorial", "description": "Membuat pintu otomatis rahasia", "tags": "minecraft redstone tutorial"},
    {"title": "Roblox tycoon game grind", "description": "Membangun bisnis virtual dan upgrade", "tags": "roblox tycoon sandbox"},

    # === Horror ===
    {"title": "FNAF full night 1 sampai 5", "description": "Bertahan dari jumpscare animatronic", "tags": "fnaf horror jumpscare"},
    {"title": "Outlast asylum escape", "description": "Kabur dengan kamera night vision", "tags": "outlast horror survival"},
    {"title": "Poppy Playtime kejar kejaran Huggy Wuggy", "description": "Menarik puzzle sambil dikejar", "tags": "poppy playtime horror"},
    {"title": "Resident Evil 4 remake village fight", "description": "Dikeroyok penduduk desa aneh", "tags": "re4 horror action"},
    {"title": "Phasmophobia ghost hunting", "description": "Mencari hantu dengan EMF dan spirit box", "tags": "phasmophobia horror co-op"},
    {"title": "Devour multiplayer horror chaos", "description": "Lari dari iblis sambil mengumpulkan item", "tags": "devour horror"},
    {"title": "Slender Man woods gameplay", "description": "Mencari kertas sambil dikejar slender", "tags": "slenderman horror"},
    {"title": "Visage psychological horror", "description": "Menjelajah rumah berhantu mengerikan", "tags": "visage horror"},
    {"title": "Little Nightmares puzzle horror", "description": "Anak kecil kabur dari monster besar", "tags": "little nightmares horror"},
    {"title": "Amnesia The Dark Descent gameplay", "description": "Berjalan di kastil gelap menakutkan", "tags": "amnesia horror"},

    # === Racing / Sports ===
    {"title": "Forza Horizon 5 drift build", "description": "Drift di tikungan tajam gunung", "tags": "forza horizon racing drift"},
    {"title": "Gran Turismo 7 circuit race", "description": "Balapan mobil sport di sirkuit resmi", "tags": "gran turismo racing sim"},
    {"title": "Need for Speed Heat street race", "description": "Balap liar malam kota", "tags": "nfs heat racing"},
    {"title": "F1 23 career mode", "description": "Menjadi pembalap Formula 1 profesional", "tags": "f1 23 racing simulation"},
    {"title": "FIFA 24 division rivals", "description": "Main online melawan pemain global", "tags": "fifa football sports"},
    {"title": "eFootball 2024 match highlight", "description": "Gol indah dari luar kotak penalti", "tags": "efootball soccer sports"},
    {"title": "NBA 2K24 mycareer guard build", "description": "Menaikkan overall pemain basket", "tags": "nba2k basketball sports"},
    {"title": "Rocket League aerial goal", "description": "Mencetak gol dengan mekanik udara", "tags": "rocket league car football"},
    {"title": "Trackmania time attack", "description": "Mengejar waktu terbaik di map sulit", "tags": "trackmania racing time trial"},
    {"title": "MotoGP racing wet track", "description": "Balapan motor di trek hujan", "tags": "motogp racing bike"},

    # === Strategy / Tactics ===
    {"title": "Clash of Clans TH15 war attack", "description": "Menggunakan strategi hybrid di CWL", "tags": "coc clash of clans strategy"},
    {"title": "Clash Royale ladder push", "description": "Naik arena dengan deck meta", "tags": "clash royale strategy"},
    {"title": "Age of Empires IV fast feudal", "description": "Membangun ekonomi dan rush musuh", "tags": "aoe4 rts strategy"},
    {"title": "Civilization VI domination victory", "description": "Menyerang kota musuh dan menang perang", "tags": "civ6 4x strategy"},
    {"title": "StarCraft II zerg rush", "description": "Strategi agresif melawan protoss", "tags": "starcraft2 rts strategy"},
    {"title": "Total War Three Kingdoms epic battle", "description": "Pertempuran skala besar", "tags": "total war strategy"},
    {"title": "XCOM 2 ironman mode", "description": "Taktik turn-based melawan alien", "tags": "xcom2 tactics strategy"},
    {"title": "Anno 1800 city building", "description": "Mengatur ekonomi dan logistik", "tags": "anno city building strategy"},
    {"title": "Heroes of Might and Magic III nostalgia", "description": "Mainkan map klasik dan duel AI", "tags": "homm3 strategy"},
    {"title": "Plants vs Zombies endless mode", "description": "Pertahanan kebun dari zombie", "tags": "pvz strategy casual"},

    # === Puzzle / Casual / Rhythm ===
    {"title": "Portal 2 co-op puzzle", "description": "Menyelesaikan test chamber bersama teman", "tags": "portal2 puzzle co-op"},
    {"title": "Tetris 99 last circle clutch", "description": "Bertahan di level tinggi sampai menang", "tags": "tetris puzzle battle royale"},
    {"title": "Candy Crush level sulit", "description": "Mencoba menembus level yang susah", "tags": "candy crush puzzle casual"},
    {"title": "OSU insane difficulty map", "description": "Main beatmap 6 stars", "tags": "osu rhythm music"},
    {"title": "Beat Saber expert+ mode", "description": "VR rhythm game dengan lagu cepat", "tags": "beat saber vr rhythm"},
    {"title": "Geometry Dash demon level", "description": "Mencoba level tersulit berulang kali", "tags": "geometry dash platformer puzzle"},
    {"title": "Human Fall Flat funny moments", "description": "Game puzzle fisika dengan ragdoll", "tags": "human fall flat puzzle"},
    {"title": "Monument Valley relaxing puzzle", "description": "Memutar struktur ilusi optik", "tags": "monument valley puzzle"},
    {"title": "Fall Guys race to the crown", "description": "Mini game lucu battle royale", "tags": "fall guys party game"},
    {"title": "Stumble Guys Indonesia room", "description": "Main bareng teman satu lobby", "tags": "stumble guys casual party"},
]

def main():
    i = 0
    while True:
        payload = random.choice(SAMPLES)
        try:
            resp = requests.post(URL, json=payload, timeout=5)
            print(i, resp.status_code, resp.json())
        except Exception as e:
            print("Error:", e)
        i += 1
        time.sleep(2)  # setiap 2 detik kirim 1 request

if __name__ == "__main__":
    main()
