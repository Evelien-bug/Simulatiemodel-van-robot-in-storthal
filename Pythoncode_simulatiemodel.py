
import simpy
import random
from collections import defaultdict
import pandas as pd

# INPUT
OBSERVATIE_TIJD = (3, 5)  # Observatietijd interval in minuten, AANPASSEN VOOR DRIE RUNS: 35, 57 en 79!
LOS_DUUR = (9, 11)  # duur van het losproces
AANTAL_STORTGATEN = 5  # Aantal stortgaten
SIMULATIE_TIJD = 960  # Simulatietijd in minuten (06:00 - 22:00 = 16 uur = 960 minuten)
AFSTANDEN = [0, 8, 16, 84, 92]  # Afstanden tussen stortgaten (meters)
VRACHTWAGEN_SNELHEID = 15 / 3.6  # Snelheid van de vrachtwagens in m/s (15 km/h)
AGV_SNELHEID_LAAG = 1.0  # AGV lage snelheid in m/s
AGV_SNELHEID_HOOG = 1.5  # AGV hoge snelheid in m/s
MAX_HAL_CAPACITEIT = 5  # Maximaal aantal vrachtwagens in de hal
ITERATIES = 7 # Aantal iteraties (dagen) voor de simulatie
AANTAL_VRACHTWAGENS_PER_DAG = 161
AANKOMST_VERDELING = [0.08811234, 0.08096077, 0.07839621, 0.07495595, 0.07518530, 0.07646758, 0.07855259, 0.07499765, 0.07415323, 0.06938899, 0.06284207, 0.05551328, 0.04217966, 0.03465279, 0.02092303, 0.01240578]


# Vrachtwagens per uur berekenen
vrachtwagens_per_uur = {}
for i in range(len(AANKOMST_VERDELING)):
    xi = round(AANTAL_VRACHTWAGENS_PER_DAG * AANKOMST_VERDELING[i])
    vrachtwagens_per_uur[f"x{i+1}"] = xi 

aankomstschema = {
    6: vrachtwagens_per_uur['x1'],
    7: vrachtwagens_per_uur['x2'],
    8: vrachtwagens_per_uur['x3'],
    9: vrachtwagens_per_uur['x4'],
    10: vrachtwagens_per_uur['x5'],
    11: vrachtwagens_per_uur['x6'],
    12: vrachtwagens_per_uur['x7'],
    13: vrachtwagens_per_uur['x8'],
    14: vrachtwagens_per_uur['x9'],
    15: vrachtwagens_per_uur['x10'],
    16: vrachtwagens_per_uur['x11'],
    17: vrachtwagens_per_uur['x12'],
    18: vrachtwagens_per_uur['x13'],
    19: vrachtwagens_per_uur['x14'],
    20: vrachtwagens_per_uur['x15'],
    21: vrachtwagens_per_uur['x16']}

afgeronde_observatie = defaultdict(list) # Lijst met alle afgeronde observaties
gegenereerde_vrachtwagens = 0 # Index toewijzen aan binnenkomende vrachtwagens
totale_reistijd = 0 # Houdt bij hoe veel de robot op een dag heeft gereden

# Lijst voor de opslag van de resultaten
resultaten = []

def bereken_afstand(x1, x2):
    """Berekent de afstand tussen twee stortgaten."""
    return abs(x1 - x2)

def genereer_vrachtwagens(env, stortgat_status, storthal_capaciteit):
    """Genereert vrachtwagens op basis van het aankomstschema."""
    global gegenereerde_vrachtwagens
    vrachtwagen_id = 0 # id toewijzen aan vrachtwagens
    for uur in range(6, 22):
        aantal_vrachtwagens = aankomstschema.get(uur, 0)
        # Willekeurige aankomsttijden binnen het uur genereren
        aankomst_tijden = sorted([random.uniform(0, 60) for _ in range(aantal_vrachtwagens)])
        vorige_tijd = 0
        for aankomst_tijd in aankomst_tijden:
            # Wachten tot de volgende vrachtwagen aankomt
            yield env.timeout(aankomst_tijd - vorige_tijd)
            vorige_tijd = aankomst_tijd
            vrachtwagen_id += 1
            gegenereerde_vrachtwagens += 1
            env.process(vrachtwagen(env, stortgat_status, storthal_capaciteit, vrachtwagen_id))

def vrachtwagen(env, stortgat_status, storthal_capaciteit, vrachtwagen_id):
    """Simuleert vrachtwagenactiviteit: Rijden, lossen en vertrekken"""
    with storthal_capaciteit.request() as verzoek:  # Wacht op toegang tot de hal
        yield verzoek
        # Vrachtwagen rijdt naar de startpositie in de hal
        rijtijd_in = 28 / VRACHTWAGEN_SNELHEID / 60  # Tijd naar de halingang
        yield env.timeout(rijtijd_in)
        # Zoekt een beschikbaar stortgat
        for _ in range(5):  # Probeer een stortgat te vinden
            beschikbare_stortgaten = [i for i, status in enumerate(stortgat_status) if status == 0]
            if beschikbare_stortgaten:
                doel_index = random.choice(beschikbare_stortgaten)  # Kies een willekeurig beschikbaar stortgat
                stortgat_status[doel_index] = vrachtwagen_id
                # Rijden naar het geselecteerde stortgat
                afstand_naar_stortgat = sum(AFSTANDEN[:doel_index + 1])
                rijtijd_naar_stortgat = afstand_naar_stortgat / VRACHTWAGEN_SNELHEID / 60
                yield env.timeout(rijtijd_naar_stortgat)
                # Losproces
                los_tijd = random.uniform(*LOS_DUUR)
                yield env.timeout(los_tijd)
                stortgat_status[doel_index] = 0 # Stortgat weer beschikbaar
                # Terugrijden naar de startpositie
                rijtijd_terug = afstand_naar_stortgat / VRACHTWAGEN_SNELHEID / 60
                yield env.timeout(rijtijd_terug)
                break
            yield env.timeout(0.001)  # Wachten en opnieuw proberen
        # Terugrijden naar de uitgang van de hal
        rijtijd_uit = 28 / VRACHTWAGEN_SNELHEID / 60  # Tijd naar de uitgang
        yield env.timeout(rijtijd_uit)

                      
def agv(env, stortgat_status, strategie, agv_snelheid):
    """Simuleert de activiteiten van de AGV (robot) volgens verschillende strategieën."""
    global totale_reistijd, afgeronde_observatie
    agv_positie = 0  # Startpositie
    midden_punt = 46  # Middenpositie van de hal (afstand in meters vanaf startpositie)
    gecontroleerde_vrachtwagens = set()  # Houdt bij welke vrachtwagens al zijn gecontroleerd
    standby_start = None  # Tijd bijhouden wanneer de AGV begint met wachten (standby staan)

    while True:
        # Beschikbare stortgaten zoeken met vrachtwagens die nog niet gecontroleerd zijn
        beschikbaar = [
            i for i, status in enumerate(stortgat_status)
            if status > 0 and status not in gecontroleerde_vrachtwagens]

        if beschikbaar:
            # Bepaal het volgende stortgat op basis van de strategie
            if strategie in ["nearest1", "nearest2"]:
                # Kies het dichtstbijzijnde stortgat
                doel_index = min(beschikbaar, key=lambda i: bereken_afstand(agv_positie, sum(AFSTANDEN[:i + 1])))
            elif strategie in ["fifo1", "fifo2"]: # (first in first out)
                # Kies het stortgat met de vrachtwagen met het laagste ID (Eerst binnengekomen vrachtwagen)
                doel_index = min(beschikbaar, key=lambda i: stortgat_status[i])
            elif strategie in ["lifo1", "lifo2"]: # (last in first out)
                # Kies het stortgat met de vrachtwagen met het hoogste ID (Laatst binnengekomen vrachtwagen)
                doel_index = max(beschikbaar, key=lambda i: stortgat_status[i])

            # De AGV rijdt naar het geselecteerde stortgat
            afstand = bereken_afstand(agv_positie, sum(AFSTANDEN[:doel_index + 1]))
            reistijd = afstand / agv_snelheid / 60
            totale_reistijd += reistijd
            yield env.timeout(reistijd)
            agv_positie = sum(AFSTANDEN[:doel_index + 1])

            # Vrachtwagen-ID ophalen
            vrachtwagen_id = stortgat_status[doel_index]
            if vrachtwagen_id not in gecontroleerde_vrachtwagens:

                # Observatieproces simuleren
                observatie_tijd = random.uniform(*OBSERVATIE_TIJD)
                yield env.timeout(observatie_tijd)

                # De observatie registreren
                afgeronde_observatie[strategie].append((env.now, doel_index, vrachtwagen_id))
                gecontroleerde_vrachtwagens.add(vrachtwagen_id)

                # Gedrag na observatie
                if strategie in ["fifo1", "nearest1", "lifo1"]:
                    # Op dezelfde positie standby staan
                    continue
                elif strategie in ["fifo2", "nearest2", "lifo2"]:
                    # Terug naar het middenpunt om daar standby te staan
                    if agv_positie != midden_punt:
                        afstand = bereken_afstand(agv_positie, midden_punt)
                        reistijd = afstand / agv_snelheid / 60
                        totale_reistijd += reistijd
                        yield env.timeout(reistijd)
                        agv_positie = midden_punt
        else:
            # Geen vrachtwagens beschikbaar: standby of rij naar middenpunt
            if strategie in ["nearest2", "fifo2", "lifo2"]:
                if agv_positie != midden_punt:
                    afstand = bereken_afstand(agv_positie, midden_punt)
                    reistijd = afstand / agv_snelheid / 60
                    totale_reistijd += reistijd
                    yield env.timeout(reistijd)
                    agv_positie = midden_punt

                if standby_start is None:
                    standby_start = env.now
                yield env.timeout(0.001)
            else:
                if standby_start is None:
                    standby_start = env.now
                yield env.timeout(0.001)


def voer_simulatie_uit_voor_strategie(strategie, agv_snelheid, iteratie, snelheid_label):
    """Voer een simulatie uit voor een specifieke strategie."""
    global afgeronde_observatie, gegenereerde_vrachtwagens, totale_reistijd
    stortgat_status = [0] * AANTAL_STORTGATEN # Stortgaten starten leeg
    env = simpy.Environment()
    storthal_capaciteit = simpy.Resource(env, capacity=MAX_HAL_CAPACITEIT) # Capaciteit van de storthal

    # Variabelen resetten voor de huidige simulatie
    afgeronde_observatie[strategie] = []
    gegenereerde_vrachtwagens = 0
    totale_reistijd = 0

    # Processen starten voor vrachtwagens en de AGV
    env.process(genereer_vrachtwagens(env, stortgat_status, storthal_capaciteit))
    env.process(agv(env, stortgat_status, strategie, agv_snelheid))
    # De simulatie runnen tot het einde van de geplande tijd
    env.run(until=SIMULATIE_TIJD)

    # Resultaten opslaan
    resultaten.append({
        "Iteratie": iteratie,
        "Snelheid": snelheid_label,
        "Strategie": strategie,
        "Totaal Observaties": len(afgeronde_observatie[strategie]),
        "Totale Reistijd": totale_reistijd})

# Iteratieve simulaties voor alle strategieën en twee snelheden
for i in range(ITERATIES):
    print(f"\nIteratie {i + 1} van {ITERATIES}:")
    for agv_snelheid, label in [(AGV_SNELHEID_LAAG, "lage snelheid (1.0 m/s)"), 
                                (AGV_SNELHEID_HOOG, "hoge snelheid (1.5 m/s)")]:
        for strategie in ["nearest1", "nearest2", "fifo1", "fifo2", "lifo1", "lifo2"]:
            voer_simulatie_uit_voor_strategie(strategie, agv_snelheid, i + 1, label)

# Resultaten exporteren naar CSV
resultaten_df = pd.DataFrame(resultaten)
resultaten_df.to_csv("simulatie_resultaten35.csv", index=False) # Per run aanpassen naar 57 of 79 (observatietijd)



