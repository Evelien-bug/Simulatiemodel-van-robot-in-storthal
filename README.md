# Simulatiemodel-van-robot-in-storthal
Een simulatiemodel om de rijstrategie en snelheid van de robot te optimaliseren, met als doel het uitvoeren van een zo hoog mogelijk percentage observaties binnen de storthal van Bedrijf A.


**Intrductie**

Bedrijf A, is een afvalverwerkingsbedrijven in Nederland en houdt zich bezig met het verwerken en omzetten van afval in energie en grondstoffen. Bedrijf A heeft geïnvesteerd in een Autonomous Guided Vehicle (AGV) om de vrachtwagens en het personeel te observeren in de storthal. Bij dit bedrijf komen dagelijks vrachtwagens binnen, indien de storthal vol is wachten ze op een groen sein waarna ze de hal binnen mogen rijden. Vervolgens wordt een vrachtwagen door een medewerker aan een stortgat toegewezen en lost deze zijn afval. Na het storten verlaten de vrachtwagens de hal onmiddellijk. Om de vrachtwagens te observeren zal een robot in een rechte lijn langs de muur rijden.



**Data**

Om inzicht te krijgen in het aankomstproces van de vrachtwagens is er een data aanvraag ingediend bij Bedrijf A van de in- en uitweeggegevens. Deze data is verkend en bewerkt om zo een verdeling van de aankomst van vrachtwagens per uur op een dag te extraheren en vervolgens te kunnen implementeren in het simulatiemodel. Daarnaast is gebruik gemaakt van data afkomstig van Bedrijf B, namelijk de twee mogelijke snelheden van de robot.



**Simulatiemodel**

De Python-code is gebruikt voor het simuleren van de prestaties van de robot en de vrachtwagens in de storthal. De code voert simulaties uit om verschillende rijstrategieën en snelheden van de robot te analyseren. De resultaten van deze simulaties geven inzicht in de meest efficiënte instellingen voor het optimaliseren van de observaties en het minimaliseren van de reistijd. De simulatie (pythoncode_simulatiemodel.py) dient drie keer uitgevoerd te worden, waarbij er drie verschillende observatietijden gesimuleert worden (3-5, 5-7 en 7-9). Deze tijden worden handmatig aangepast van (3,5) naar (5,7) en (7,9). Let op: Bij elke run moet de bestandsnaam die opgeslagen wordt veranderd worden naar de getallen van de bijbehorende observatietijd: simulatie_resultaten35, simulatie_resultaten57 en simulatie_resultaten79.



**Uitvoering en resultaten**

Vervolgens kan code voor het verkrijgen van de resultaten (pythoncode_resultaten_simulatie.py) worden uitgevoerd om resultaten te genereren van de simulatie.



**Variabelenlijst**

- OBSERVATIE_TIJD = Hoe lang de robot over een observatie mag doen. Een observatie is het controleren van de veiligheidseisen van personeel en de stortlocatie van een vrachtwagen.

LOS_DUUR = Hoe lang een vrachtwagen doet over het lossen van afval.

AANTAL_STORTGATEN = Aantal stortgaten die tegelijk open mogen zijn in de storthal.

SIMULATIE_TIJD = In dit onderzoek worden de openingstijden van de storthal gehanteerd. Een simulatie is 1 werkdag. Simulatietijd in minuten (06:00 - 22:00 = 16 uur = 960 minuten).
AFSTANDEN = Afstanden tussen stortgaten (meters). Dit wordt bijgehouden om te controleren of de robot een volledige werkdag kan rijden op een volledig opgeladen batterij. Daarnaast wordt er rekening gehouden met de afstanden die vrachtwagens afleggen.
VRACHTWAGEN_SNELHEID = Max toegestane snelheid van de vrachtwagens in de storthal m/s (15 km/h).
AGV_SNELHEID_LAAG = AGV lage snelheid in (1 m/s).
AGV_SNELHEID_HOOG = AGV hoge snelheid in (1,5 m/s).
MAX_HAL_CAPACITEIT = Maximaal aantal vrachtwagens dat tegelijk in de hal aanwezig mag zijn.
ITERATIES = Aantal iteraties (dagen) voor de simulatie
AANTAL_VRACHTWAGENS_PER_DAG = Het aantal vrachtwagens dat per dag gemiddeld de storthal binnenkomt. (Verkregen uit de data)
AANKOMST_VERDELING = Per uur van de dag is er berekend welk percentage van AANTAL_VRACHTWAGENS_PER_DAG er binnenkomt.
