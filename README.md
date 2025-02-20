# Simulatiemodel-van-robot-in-storthal
Een simulatiemodel om de rijstrategie en snelheid van de robot te optimaliseren, met als doel het uitvoeren van een zo hoog mogelijk percentage observaties binnen de storthal van Bedrijf A.

**Intrductie**

Bedrijf A, is een afvalverwerkingsbedrijven in Nederland en houdt zich bezig met het verwerken en omzetten van afval in energie en grondstoffen. Bedrijf A heeft geïnvesteerd in een Autonomous Guided Vehicle (AGV) om de vrachtwagens en het personeel te observeren in de storthal. Bij dit bedrijf komen dagelijks vrachtwagens binnen, indien de storthal vol is wachten ze op een groen sein waarna ze de hal binnen mogen rijden. Vervolgens wordt een vrachtwagen door een medewerker aan een stortgat toegewezen en lost deze zijn afval. Na het storten verlaten de vrachtwagens de hal onmiddellijk. Om de vrachtwagens te observeren zal een robot in een rechte lijn langs de muur rijden.


**Data**

Om inzicht te krijgen in het aankomstproces van de vrachtwagens is er een data aanvraag ingediend bij Bedrijf A van de in- en uitweeggegevens. Deze data is verkend en bewerkt om zo een verdeling van de aankomst van vrachtwagens per uur op een dag te extraheren en vervolgens te kunnen implementeren in het simulatiemodel. Daarnaast is gebruik gemaakt van data afkomstig van Bedrijf B, namelijk de twee mogelijke snelheden van de robot.


**Simulatiemodel**

De Python-code is gebruikt voor het simuleren van de prestaties van de robot en de vrachtwagens in de storthal. De code voert simulaties uit om verschillende rijstrategieën en snelheden van de robot te analyseren. De resultaten van deze simulaties geven inzicht in de meest efficiënte instellingen voor het optimaliseren van de observaties en het minimaliseren van de reistijd. 


**Uitvoering en resultaten**

De simulatie (pythoncode_simulatiemodel.py) dient drie keer uitgevoerd te worden, waarbij er geïtereerd wordt over drie verschillende observatietijden. Deze tijden worden handmatig aangepast van (3,5) naar (5,7) en (7,9). Hierbij dient de laatste regel in de code voor elke simulatie aangepast te worden: simulatie_resultaten35 naar simulatie_resultaten57 en simulatie_resultaten79. Vervolgens kan code voor het verkrijgen van de resultaten (pythoncode_resultaten_simulatie.py) worden uitgevoerd om resultaten te genereren van de simulatie.
