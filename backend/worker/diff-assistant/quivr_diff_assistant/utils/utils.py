from langchain_core.prompts.prompt import PromptTemplate

COMPARISON_PROMPT = PromptTemplate.from_template(
    template="""
    You are provided with two texts <text 1> and <text 2>. You need to consider the information contained in \
            <text 1> and compare it with the corresponding information contained in <text 2>. \
            Keep in mind that <text 2> contains non-relevant information for this task, and that in <text 2> you \
                 should only focus on the information correspnding to the information contained in <text 1>. \
                    You need to report all the differences between the information contained in <text 1> and <text 2>. \\ 
                    Your job is to parse these differences and create a clear, concise report. \
        Organize the report by sections and provide a detailed explanation of each difference. \
            Be specific on difference, it will be reviewed and verified by a highly-trained quality engineer.
    Here are the different sections of the report:
    * Dénominations, comprenant:
        * dénomination légale: nom du produit tel qu’il est défini par la réglementation, \
            en général cela inclut aussi avec des information sur son état (cuite, cru, gelé ... )
        * dénomination commercial: nom du produit tel qu’il est vendu au consommateur
    * Ingrédients et allergènes (si presents dans plusieurs langues, comparer langue par langue), comprenant:
        * liste d’ingrédients
        * traces d’allergènes
        * une sous-section pour chaque sous produit si il y a lieu;
    * Eléments de traçabilité, comprenant:
        * le code-barre EAN
        * le code article
        * numéro de lot
        * date de fabrication
        * adresse de l'entreprise
    * Conseils d’utilisation / de manipulation produit, comprenant :
        * Conditions / conseils de remise en oeuvre
        * Durée de vie
        * Durée de conservation (à compter de la date de production, à température ambiante / réfrigérée)
        * DDM - date de durabilité minimale
        * Conditions de transport
        * Conditions de conservation : « A conserver à -18°C / Ne pas recongeler un produit décongeler »
        * Temps de decongelation
        * Temperature de prechauffage
    * Caractéristiques / parametres physiques produit (unité de négoce), comprenant:
        * poids de la pièce
        * dimensions de la pièce
        * poids du produit / unité de négoce (typiquement, carton)
        * dimensions du produit / unité de négoce (typiquement, carton)
        * nombre de pièces par unité de negoce (typiquement, carton) / colis  
        * poids du colis / carton
    * Données palettisation / donnée technique sur palette (unité de transport)
        * hauteur palette
        * dimensions de l'unité de negoce (typiquement, carton) / colis
        * nombre de colis par couche / palette
    * Valeurs / informations nutritionnelles
    * Autres

    Notes: 
     -> Coup de Pates: Tradition & Innovation, est l'entreprise productrice / marque du produit.

    Chaque sections doivent être organisées comme suit :
    ## Section name
    **<text 1>** :
        * ...
        * ...

    **<text 2>** : ...
        * ...
        * ...

    **Differences**: 
        * ...
        * ...


    Beginning of <text 1>
    {document}
    End of <text 1>

    
    Beginning of <text 2> 
    {cdc}
    End of <text 2>


    You need to consider all the information contained in <text 1> and compare it \
        with the corresponding information contained in <text 2>.
    The report should be written in a professional and formal tone and in French \
        and it should follow the structure outlined above. If <text 1> doesn't contain a particular information, \
        then you should ignore that information for <text 2> as well and avoid reporting any differences.

    In the report you should replace evry occurence of <text 1> with {text_1} and every occurence of <text 2> with {text_2}.
        
    ## Dénominations
    **{text_1}** :
        * 
    """
)
