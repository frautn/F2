# Guías de ejercicios

## Lista de ejercicios seleccionados

Para imprimir una lista de ejercicios seleccionados (para hacer en clase por ejemplo), modificar la variable:  
guias_newcommands: {\seleccionados}{true}

Los ejercicios seleccionados son los que tienen:  
\ifthenelse{\equal{\seleccionados}{true}}{\addToList{xyz}{\ExerciseHeaderNB}}{}  

Ubicar \printList{xyz} en el lugar donde se quiera generar la lista.

## Generar una guía con espacio para anotar

Con espacio para anotar:
\usepackage[a4paper,paperwidth=847pt, textheight=650pt, textwidth=418pt,top=2.5cm,bottom=2.5cm]{geometry}
\setlength{\oddsidemargin}{17pt}
\setlength{\marginparwidth}{250pt}

## Símbolo de pregunta teórica

\textbf{\raisebox{.5pt}{\textcircled{\raisebox{-1.2pt} {T}}}}

## Paquetes removidos que pueden ser útiles

\usepackage{ucs}  
\usepackage[utf8x]{inputenc}  
\usepackage{pdfpages}  
\usepackage{tikz}  % Incluido en circuitikz.  
\usepackage{ifthen}  
\usepackage{subfigure}  
\usepackage{gnuplottex}  
\usepackage[stable]{footmisc} %para footnote dentro de pma  
\usepackage{mathrsfs}  
\usepackage{amssymb}  
\usepackage[T1]{fontenc}  
\usepackage{bm}  % Makes the hat bold.  

## Useful links

https://pgfplots.sourceforge.net/gallery.html

https://ctan.org/pkg/pgf?lang=en
