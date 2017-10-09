# Projet	Programmation	Concurrente – année	2017 - 18	

# Polytech’Nice	Sophia	– SI

# M. Riveill

**Durée	indicative	:** entre	 15	 et	30 heures dont	uniquement	 6	 heures	seront	faites	lors	des	séances	de	
TD. A	faire	par	groupe	de	deux.

**Vision	d’ensemble	du	projet :** il	s’agit	de	modéliser	de	manière	simple	le	déplacement	d’une	foule.	
Nous	sommes	dans	le	cadre	d’un	cours	programmation	concurrente	et	donc	ce	qui	est	important	ce	
n’est	ni	l’IHM,	ni	l’évolutivité	du	code	mais	bien	l’identification	des	contraintes	de	synchronisation	et	
y	apporter	une	réponse	adéquate.
Vous	pouvez	programmer	ce	projet	dans	les	langages	suivants :	Python,	GO,	C,	C++	mais	pas	Java.	Si	
vous	choisissez	C/C++	alors	vous	devrez	utiliser	la	bibliothèque	Posix	pour	gérer	les	threads	et	la	
synchronisation.

**Spécification	de	la	mise	en	œuvre**

Le	terrain sur	lequel	se	déplace	la	foule	fait	512	pixels	x	128	pixels	et	sera	représenté	par	une	matrice	
de	taille	identique	ayant	512	colonnes	(numérotées	de	0	à	511)	et	de	128	lignes	(numérotée	de	0	à	
127 ). Des	obstacles	de	taille	quelconque	seront	présent	sur	le	terrain.	En	aucun	cas	ces	obstacles	
touchent	le	bord	du	terrain.	La	sortie	sera	le	coin	supérieur	gauche	et	fera	2	pixels	*	2	pixels.	La	
figure	1	ci-dessous	représente	le	terrain.

```
Fig.	1	– forme	du	terrain
```
Une	personne	fait	1*1 pixel	et	se	déplace	d’un	seul	pixel	selon	les	directions	Nord,	Sud,	Est	et	Ouest	
ainsi	que	les	4	diagonale	Nord-Sud,	Nord-Ouest,	Sud-Est	et	Sud-Ouest.	

Après	 une	 phase	 d’initialisation	 qui	 met	en	 place	 le	 terrain	 et	 qui	distribue	 aléatoirement	 2P
personnes,	le	simulateur	fait	avancer	chacune	des	personnes	vers	la	sortie.	A	chaque	déplacement	la	
personne	doit	se	rapprocher	de	la	sortie. Pour	simplifier	le	déplacement	des	personnes,	un	point	


azimuth	 sera	 fixé	(par	 exemple	 l’angle	en	 haut	 à	 gauche)	et	 le	 déplacement choisi	 sera	 le	
déplacement	 **possible** qui	minimise	la	distance	avec	le	point	(cf.	figure	3).	Bien	évidemment	une	
personne	ne	peut	pas	occuper	une	place	occupée.

```
Fig.	3	– point	azimuth
```
Afin	de	comparer	les	différentes mises	en	œuvres,	il	est	souhaitable	qu’à	chaque	exécution,	les	
personnes	partent	de	la	même	place.

**Mises-en œuvre :** vous	allez	programmer	un	simulateur	ultra-simpliste	du	déplacement	d’une	foule.
Toutes	les versions	seront	intégrées	dans	le	même	code et des	options	du	programme	permettront	
de	choisir	la	version	à	exécuter :

- p	[0123456789]	:	nombre de	personnes	présentent sur	le	terrain
- p varie	de	0	à	9	et	le	nombre	de	personnes	vaut	2p (i.e.	varie	de	1	à	512)
- t	[01]	: scénario	de	créations	des	threads
- - t0	:	une	thread	est	associée	à	chacune	des	personnes	créées	et	chaque	thread	doit	faire	
    avancer	la	personne	qu’elle	gère ;
- - t1 :	le	terrain	est	partagé	en	4	partie	égale.	Une	thread	est	associée	à	chaque	partie	du	
    terrain	et	chaque	thread	doit	faire	avancer	successivement	chacune	des	personnes	présentes	
    sur	la	portion	de	terrain	que	la	thread	gère.
- m :	mesure	du	temps	d’exécution
- mesure	la	consommation	du	CPU	et	le	temps	de	réponse	du	programme
- lorsque	des	mesures	sont	effectuées :	la	phase	d’initialisation	du	programme	n’est	pas	prise	
    en	compte	et	l’affichage	n’est	pas	actif
- pour	effectuer	les	mesures,	l’application	est	lancée	5	fois	et	la	mesure	est	la	moyenne	des	3	
    valeurs	intermédiaires

Pour	simplifier	la	portabilité	des	programmes	entre	votre	machine	et	la	mienne,	il	doit	être	possible	
de	compiler	votre	programme	sans	inclure	la	partie	graphique	qui	doit	visualiser	le	déplacement	de	
la	foule	sur	le	terrain.

**Le	rendu	du	projet :**
Le	rapport	doit :

- présenter	les	threads	et	les	primitives	de	synchronisation	du	langage	utilisé
- contenir	les	algorithmes	(pseudo	code)	mis	en	œuvre


- insister	sur	la	mise	en	ouvre	de	la	synchronisation	dans	les	deux	scénarios	choisis
- décrire	les	performances	obtenues	(comment	évoluent	le	temps	de	réponse	de	l’application
    par	rapport	au	temps	de	consommation	CPU,	...)	et	avoir	un	esprit	critique	sur	la	mise	en	
    œuvre (est-ce	ce	que	l’on	attendait ?,	...)
- vous	rendrez	2	rapports
    o le	premier	portera	sur	la	mise	en	œuvre	du	scénario	t0	(1	thread	par	personne)
    o le	 second,	 sera	 un	 rapport	 global	 et	 portera	 sur	 les	 deux	 scénarios	 avec	 une	
       comparaison	de	l’ensemble


**Quelques	primitives	pour	mesurer	le	temps en	posix,	 vous	 pouvez	 bien	 évidemment	en	utiliser	
d’autres...**

```
clock_t **clock** (void);
The	 **clock** ()	function	determines	the	amount	of	processor	time	used	since	the	invocation	of	the	
calling	process,	measured	in	CLOCKS_PER_SECs	of	a	second.
La	commande	clock vous	permet	de	calculer	le	temps	CPU	consommé.

time_t **time** (time_t *tloc);
The	 **time** ()	function	returns	the	value	of	time	in	seconds	since	0	hours,	0	minutes,	0	seconds,	
January	1,	1970,	Coordinated	Universal	Time,	without	including	leap	seconds.
La	commande	time	vous	permet	de	calculer	le	temps de	réponse.

int	 **gettimeofday** (struct	timeval	*restrict	tp,	void	*restrict	tzp)
La	commande	gettimeofday vous	permet	de	calculer	le	temps	de	réponse.

Int **getrusage** (int who,	struct rusage *r_usage);
**getrusage** ()	returns	information	describing	the	resources	utilized	by	the	current	process,	or	all	
its	 terminated	 child	 processes.	 The	 who parameter	 is	 either	 RUSAGE_SELF	 or	
RUSAGE_CHILDREN.		The	buffer	to	which	r_usage points	will	be	filled	in	with	the	following	
structure:
struct	rusage	{
struct	timeval	ru_utime;	/*	user	time	used	*/
struct	timeval	ru_stime;	/*	system	time	used	*/
long	ru_maxrss;										/*	max	resident	set	size	*/
long	ru_ixrss;											/*	integral	shared	text	memory	size	*/
long	ru_idrss;											/*	integral	unshared	data	size	*/
long	ru_isrss;											/*	integral	unshared	stack	size	*/
long	ru_minflt;										/*	page	reclaims	*/
long	ru_majflt;										/*	page	faults	*/
long	ru_nswap;											/*	swaps	*/
long	ru_inblock;									/*	block	input	operations	*/
long	ru_oublock;									/*	block	output	operations	*/
long	ru_msgsnd;										/*	messages	sent	*/
long	ru_msgrcv;										/*	messages	received	*/
long	ru_nsignals;								/*	signals	received	*/
long	ru_nvcsw;											/*	voluntary	context	switches	*/
long	ru_nivcsw;										/*	involuntary	context	switches	*/
};
Les	deux	premiers	paramètres	vous	permettent	de	calculer	le	temps	CPU	consommé	et	le	
troisièmes	l’empreinte	maximale	de	votre	programme.

Int **getopt** (int argc,	char * const argv[],	const char *optstring);
The	 **getopt** ()	function	incrementally	parses	a	command	line	argument	list	argv and	returns	the	
next	known option	character.		An	option	character	is	known if	it	has	been	specified	in	the	
string	of	accepted	option	characters,	optstring.
La	commande	getopt	vous permet	d’analyser	les	paramètres	utiliser	lors	du	‘lancement’	du	
processus.
```

## Authors

[Clément Béal](mailto:clement.beal@etu.unice.fr)
[Maxime Flament](mailto:maxime.flament@etu.unice.fr)
[Grégory Merlet](mailto:gregory.merlet@etu.unice.fr)