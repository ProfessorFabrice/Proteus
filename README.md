# Proteus

On distingue deux types de morphologie, la morphologie flexionnelle ou
grammaticale et la morphologie lexicale. La première concerne des
variations liées au contexte, comme les phénomènes d'accord en genre et
en nombre ou encore la conjugaison des verbes. La morphologie lexicale
concerne la formation même des mots souvent à partir d'un lexème auquel
on associe des préfixes ou des suffixes. Cependant, la frontière entre
analyse lexicale et syntaxique, voire sémantique, est perméable et
l'identification d'un mot, quel que soit le sens qu'on lui donne, peut
nécessiter l'utilisation de ressources lexicales, syntaxiques ou
sémantiques. Il y a donc une problématique de prise en compte plus ou
moins importante du contexte. Si les mots simples peuvent aisément être
traités à l'aide d'informations non contextuelles, il n'en est pas de
même pour les unités polylexicales.

[Proteus]{.sans-serif} est un système permettant de représenter le
lexique de manière efficace, non seulement du point de vue de la
création de la ressource, mais aussi du point de vue de la cohérence
linguistique. Au niveau flexionnel il propose un mécanisme de
transformation simple, multilingue et adapté aux formes simples et
composées. Il peut être utilisé aussi bien pour générer des formes
simples que pour les analyser. Au niveau du lexique proprement dit, le
modèle permet d'effectuer des regroupements de flexions.

Nous distinguons donc trois niveaux :

-   la flexion à proprement parler : comment à partir d'une forme
    initiale est-il possible d'arriver à une forme dérivée ? L'unité de
    traitement atomique est ici le caractère et les règles de
    transformation s'appliquent localement ;

-   comment organiser les règles pour les regrouper efficacement en
    familles de manière à éviter la redondance qui est source
    d'erreurs ? L'unité de traitement atomique est ici la règle de
    transformation ;

-   quelles sont, une fois la forme dérivée construite, les opérations à
    effectuer pour rendre cette forme valide par rapport à des règles ?
    L'unité de traitement est ici le token. Cette étape permet de rendre
    compte, étant donnée une langue, des particularismes phonologiques
    qui ne dépendent ni de la flexion ni de la racine.

Le modèle a été élaboré de manière à répondre aux attendus suivants :

1.  Une description *in extenso* de la langue ne permet pas d'effectuer
    l'analyse des mots nouveaux mais dont la flexion est régulière. Il
    faut donc mettre en place un modèle de flexion qu'il sera possible
    d'utiliser aussi bien en analyse qu'en génération. L'analyse de mots
    est possible non seulement sur les mots connus mais aussi sur les
    mots inconnus.

2.  Dans une base lexicale, où le nombre d'éléments atteint le million
    pour le français, la présence d'une erreur est toujours possible,
    voire inévitable. Il faut par conséquent envisager une procédure de
    maintenance efficace. La ressource sur laquelle portera cette
    maintenance devra donc être constituée non pas de l'ensemble des
    formes fléchies, qui est un résultat en lecture seule, mais d'un
    dictionnaire de lemmes lié à un dictionnaire de flexions.

3.  La notion de mot est complexe de sorte que se limiter aux seuls mots
    simples n'est pas suffisant. Le modèle de flexion doit intégrer la
    gestion aussi bien des mots simples que celle des mots polylexicaux.
    La seule limite que nous nous fixons est d'ordre syntaxique : la
    gestion du figement, même si elle est fondamentale, requiert la mise
    en œuvre d'autres outils.

4.  Les transformations morphologiques diffèrent suivant la langue. Nous
    devons construire un système capable de simplement rendre compte des
    transformations aussi bien préfixales que suffixales ou infixales.
    Le traitement de l'arabe est de ce point de vue un bon indicateur
    puisque l'on y retrouve les trois types de modifications.

5.  Une règle de flexion, appliquée sur un mot, n'est jamais
    complètement autonome, mais s'inscrit dans le cadre d'un ensemble.
    On regroupera par exemple dans un même groupe l'ensemble des
    conjugaisons d'un type de verbe, et ce pour tous les temps. Cette
    manière de faire va faciliter la conception, la maintenance et
    l'utilisation des règles.

6.  La flexion ne se limite pas toujours à des transformations
    morphologiques. Des phénomènes phonologiques peuvent intervenir.
    Plus généralement il existe des traitements à appliquer sur les
    formes fléchies qui ne peuvent être modélisés simplement à partir
    des règles.

7.  Le modèle proposé doit s'appuyer sur un ensemble d'outils simples et
    doit pouvoir s'intégrer facilement au sein d'applications tierces et
    permettre une utilisation des dictionnaires produits dans un autre
    environnement.

Pour la manipulation des caractères le principe est identique dans
l'esprit à ce que proposent Unitex/Intex/Nooj. Le modèle proposé
s'appuie sur un ensemble d'opérateurs sur les caractères d'une *liste*
via l'utilisation d'une *pile*. L'application, dans un certain ordre, de
ces opérateurs forme un *code* et permet de produire une *forme
fléchie*. Le code lui-même est composé d'une suite ordonnée d'opérateurs
élémentaires.

En simplifiant le modèle à l'extrême, l'utilisation d'une règle à partir
d'un lemme (i) effectue un déplacement de caractères de la liste vers
une pile ou inversement (ii) en effaçant ou en insérant des caractères.
Par défaut, les opérations s'appliquent sur les caractères placés en fin
de mot ou, selon l'opérateur, en haut de la pile de caractères. Les
opérateurs élémentaires peuvent être inversés, ce qui permet
l'application de la fonction réciproque et de faire l'analyse de formes
fléchies.

Les différents opérateurs exprimant une transformation doivent être
suffisamment nombreux pour avoir la puissance d'expression nécessaire à
représenter tout type de flexion, mais suffisamment restreints pour ne
pas rendre la tâche d'écriture de la règle trop délicate.

::: description
`P` (Push) : déplacement d'un caractère de la liste vers la pile

`D` (Dump) : déplacement d'un caractère de la pile vers la liste

`\x\` : effacement du caractère *x*, cette opération n'est possible que
si le caractère est en fin de liste[^1]

`/x/` : ajout du caractère *x* à la fin de la liste
:::

Pour simplifier l'écriture du code, il est possible d'indiquer le nombre
de répétitions d'un opérateur avant celui-là. Le
tableau [1](#T2){reference-type="ref" reference="T2"} montre toutes les
étapes de l'application d'un code qui permet la flexion des verbes du
type de *céder* (comme *révéler*, *espérer*, ...).

::: center
::: {#T2}
   Étape  Mot          Pile    Code restant
  ------- ---------- ------ -------------------
     1    céder              `3P\é\/è/3D/ais/`
     2    cé            der   `\é\/è/3D/ais/`
     3    c             der    `/è/3D/ais/`
     4    cè            der      `3D/ais/`
     5    cèder                   `/ais/`
     6    cèderais                    

  : Génération d'une forme fléchie à partir d'un code
:::
:::

Étapes :

1$\rightarrow$`<!-- -->`{=html}2

:   : empilement de trois caractères

2$\rightarrow$`<!-- -->`{=html}3

:   : effacement d'un caractère

3$\rightarrow$`<!-- -->`{=html}4

:   : ajout d'un caractère

4$\rightarrow$`<!-- -->`{=html}5

:   : dépilement de trois caractères

5$\rightarrow$`<!-- -->`{=html}6

:   : ajout de trois caractères

La duplication de consonne étant un phénomène courant, nous introduisons
un opérateur spécifique

::: description
`C` (Clone) : duplique le dernier caractère de la liste
:::

Le code `C/e/` permet de générer la forme féminine de mots tels que
*sujet* ou *nouvel*. Le code `C/ing/` permet de générer le participe
présent de mots tels que *run*, *sit* ou *stop*.

La gestion des préfixes/suffixes nécessite aussi l'ajout d'opérateurs :

::: description
`]` (Rempli) : transfère tous les caractères de la liste vers la pile

`[` (Vide) : transfère tous les caractères de la pile vers la liste
:::

L'opérateur `]` permet de préparer un ajout en début de mot puisque tous
les caractères, quel que soit leur nombre, sont ajoutés à la pile. Nous
sommes maintenant en mesure de décrire les flexions de la forme :
*variole* $\rightarrow$ *antivariolique*. La transformation :

`enlever le caractère ’e’ en fin de mot, ajouter ’anti’ en début de mot puis ’ique’ en fin de mot`

s'écrit donc `\e\]/anti/[/ique/`. Ce même code peut ainsi analyser des
noms de vaccins de maladies comme *antirougeolique* ou *antirubéolique*.

# Un outil : Proteus

Nous avons défini un langage de description de flexions sous forme d'une
DTD XML afin de gérer par familles les différents codes tels que décrits
dans la précédente section. Il est nécessaire de regrouper plusieurs
transformations, masculin/féminin ou singulier/pluriel pour les noms et
les adjectifs ou l'ensemble des formes de la conjugaison pour les
verbes. Ces regroupements peuvent refléter un comportement standard
mais, et c'est souvent le cas, on rencontre un certain nombre de
variations par rapport à cette description *normale*. Nous avons donc
mis en place un mécanisme pour décrire ces exceptions. En ce sens, nous
nous rapprochons d'une description *à la Bescherelle* qui donne en
premier lieu la conjugaison prototypique, puis énumère les exceptions.

Une flexion est définie par :

-   un identifiant de flexion (attribut `id`) qui sera par la suite
    utilisé par le langage de description ;

-   un type (attribut optionnel `type`) qui catégorise la flexion dans
    l'arbre de description (`final` désigne une racine, `term` une
    feuille, `nonterm` un nœud interne) ;

-   un nom (élément optionnel `<name>`) correspondant à l'étiquette
    associée à la forme fléchie ;

-   des informations (élément optionnel `<info>`) sur la règle de
    flexion, ce champ tient lieu de commentaire associé à la
    description ;

-   un code de transformation [Proteus]{.sans-serif} (élément `<code>`).

Par exemple, la définition suivante permet d'associer l'identifiant
[n-y-p]{.sans-serif} avec le code `\y\/ies/`.

    <flex id="n-y-p" type="final">
        <name>Np</name>
        <info>Noun plural with 
              a terminal y</info>
        <code>\y\/ies/</code>
    <\flex>

Il est possible de regrouper sous un même identifiant plusieurs
flexions. Prenons comme exemple la conjugaison d'un verbe du premier
groupe au présent. La terminaison prototypique peut être donnée de la
manière suivante :

        <flex id="v1ip" type="term">
            <name>Vip</name>
            <info>verbes indicatif présent</info>
            <flex id="p1ns">
                <name>1s</name>
                <code>/e/</code>
            </flex>
            <flex id="p2ns">
                <name>2s</name>
                <code>/es/</code>
            </flex>
            <flex id="p3ns">
                <name>3s</name>
                <code>/e/</code>
            </flex>
            <flex id="p1np">
                <name>1p</name>
                <code>/ons/</code>
            </flex>
            <flex id="p2np">
                <name>2p</name>
                <code>/ez/</code>
            </flex>
            <flex id="p3np">
                <name>3p</name>
                <code>/ent/</code>
            </flex>
        </flex>

Cette structure regroupe l'ensemble des flexions d'un temps donné.
Chacune d'elle est associée à son propre identifiant préfixé de
l'identifiant de la structure encadrante, séparée à l'aide du caractère
point (`.`), et associée à un nom qui est lui aussi le résultat d'une
concaténation. Il est à noter que si l'identifiant est unique, le nom
peut ne pas l'être[^2]. Ce mécanisme permet l'expression de variantes
dans un paradigme (cf. infra). La
table [2](#TABCONJ){reference-type="ref" reference="TABCONJ"} présente
les résultats obtenus.

::: center
::: {#TABCONJ}
  identifiant   étiquette   code
  ------------- ----------- ---------
  `v1ip.p1ns`   `Vip1s`     `/e/`
  `v1ip.p2ns`   `Vip2s`     `/es/`
  `v1ip.p3ns`   `Vip3s`     `/e/`
  `v1ip.p1np`   `Vip1p`     `/ons/`
  `v1ip.p2np`   `Vip2p`     `/ez/`
  `v1ip.p3np`   `Vip3p`     `/ent/`

  : Règle de flexions
:::
:::

L'ensemble des temps de l'indicatif a été décrit de la même manière.
Nous introduisons un nouvel élément *opérateur* (`<op>` avec l'attribut
`add`) dont le rôle ici est de regrouper ces différentes conjugaisons.
Le principe de construction de l'identifiant implique que tous les
identifiants des codes de conjugaison de l'indicatif aient le même
préfixe.

        <flex id="vig1-1" type="nonterm">
            <name></name>
            <info>premier groupe verbe indicatif</info>
            <op type="add">
                <item value="v1ip"/>
                <item value="v1ii"/>
                <item value="v1ips"/>
                <item value="v1ifs"/>
            </op>
        </flex>    

À ce stade, pour rendre la description utilisable à partir de la forme
canonique traditionnelle, *i.e.* l'infinitif pour les verbes, il est
nécessaire de supprimer les lettre `er` en fin de mot. Il faut donc
modifier l'ensemble des codes de la classe. Cette opération est
effectuée par concaténation des codes de transformation comme dans
l'exemple ci-dessous.

      <flex id="v1" type="final">
          <name></name>
          <info>verbes du premier groupe</info>
          <op type="conc" value="vig1-1">
              <item pos="p">\re\</item>
          </op>
      </flex>

Dans cet exemple le code `\re\` (enlever *er*) est ajouté devant (valeur
`p` de l'attribut `pos`) l'ensemble des codes dont l'identifiant est
préfixé par `vig1-1`.

Dans certains cas, la modification doit être effectuée sur une flexion
particulière. Cela se fait via l'application d'un *masque* qui opère sur
un ensemble de flexions et applique des changements, possiblement de
manière sélective, sur les codes de transformation. Un masque est donc
l'ensemble des règles appliquées sur le code. Une expression régulière
sur l'identifiant (attribut `ervalue`) permet d'effectuer la sélection.
La modification du code [Proteus]{.sans-serif} se fait en appliquant un
code [Proteus]{.sans-serif}. Cette mise en abyme semble inconsistante,
puisque un code a été conçu pour s'appliquer sur un élément de langue.
Cependant il nous a paru inadéquat d'introduire une nouvelle syntaxe de
transformation. Une conséquence de ce choix est la présence de
caractères d'échappement rendant certaines règles de transformations
humainement délicates à interpréter.

La définition ci-dessous permet d'ajouter la lettre *e* à une forme
fléchie afin de maintenir sa prononciation `[``]`.

    <mask id="m-ge">
     <info>ajouter la lettre "e" après un "g"</info>
      <item ervalue="v1ip\.p1np">]5D/e/[</item>
      <item ervalue="v1ii\.p([123]ns|3np)">]5D/e/[</item>
      <item ervalue="v1if\.p([12]n[ps]|3np)">]5D/e/[</item>
    </mask>

La définition précédente transforme les code de la manière suivante :

`\er\/ons/` $\rightarrow$ `\er\/eons/`, `\re\/ais/` $\rightarrow$
`\re\/eais/`, ...

Le masque est utilisé en combinaison avec l'attribut `mask` dans une
définition de manière similaire à l'attibut `conc`.

      <flex id="v1" type="final">
          <name></name>
          <info>verbes en "er"</info>
          <op type="mask" value="vig1-1">
              <item value="m-ge"/>
          </op>
      </flex>

Il est ainsi possible de construire des flexions complexes en utilisant
une base et en appliquant une succession de masques. Ainsi, la
conjugaison du verbe *neiger* peut être exprimée par l'application de
deux masques sur la conjugaison standard. Le premier effectue des
modifications pour tenir compte de la prononciation du `[``]` et le
second supprime des codes pour tenir compte de la défectivité des verbes
météorologiques.




[^1]: L'opérateur `E` (Erase) qui efface n'importe quel caractère est
    aussi disponible, cependant son utilisation ne permet pas la
    réversibilité du processus.

[^2]: Dans l'exemple précédent l'identifiant `v1ip.p1ns` est associé au
    code `/e/` et au nom `Vip1s`
