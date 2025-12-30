#!/usr/bin/env python3
"""
Script d'analyse des feedbacks TP OREI
Analyse les fichiers JSON générés par le formulaire HTML
"""

import json
import os
from pathlib import Path
from collections import Counter
import statistics

def load_responses(folder_path="./responses"):
    """Charge tous les fichiers JSON du dossier responses"""
    responses = []
    path = Path(folder_path)
    
    if not path.exists():
        print(f"⚠️ Dossier '{folder_path}' introuvable!")
        print("Créez un dossier 'responses' et mettez-y tous les fichiers JSON")
        return responses
    
    json_files = list(path.glob("*.json"))
    
    if not json_files:
        print(f"⚠️ Aucun fichier JSON trouvé dans '{folder_path}'")
        return responses
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                responses.append(data)
        except Exception as e:
            print(f"⚠️ Erreur lecture {json_file.name}: {e}")
    
    print(f"✅ {len(responses)} réponses chargées\n")
    return responses

def analyze_scale_question(responses, key, question_text):
    """Analyse une question avec échelle (1-5 ou 0-10)"""
    values = [int(r[key]) for r in responses if key in r and r[key]]
    
    if not values:
        print(f"⚠️ Aucune réponse pour: {question_text}")
        return
    
    print(f"\n📊 {question_text}")
    print(f"   Moyenne: {statistics.mean(values):.2f}")
    print(f"   Médiane: {statistics.median(values)}")
    print(f"   Min: {min(values)} | Max: {max(values)}")
    
    # Distribution
    counts = Counter(values)
    print("   Distribution:")
    for value in sorted(counts.keys()):
        bar = "█" * counts[value]
        pct = (counts[value] / len(values)) * 100
        print(f"      {value}: {counts[value]:2d} ({pct:5.1f}%) {bar}")

def analyze_choice_question(responses, key, question_text):
    """Analyse une question à choix multiples"""
    values = [r[key] for r in responses if key in r and r[key]]
    
    if not values:
        print(f"⚠️ Aucune réponse pour: {question_text}")
        return
    
    print(f"\n📊 {question_text}")
    counts = Counter(values)
    
    for choice, count in counts.most_common():
        pct = (count / len(values)) * 100
        bar = "█" * int(pct / 3)
        print(f"   • {choice:<25}: {count:2d} ({pct:5.1f}%) {bar}")

def analyze_multiselect(responses, key, question_text):
    """Analyse une question multi-sélection"""
    all_choices = []
    for r in responses:
        if key in r and r[key]:
            if isinstance(r[key], list):
                all_choices.extend(r[key])
            else:
                all_choices.append(r[key])
    
    if not all_choices:
        print(f"⚠️ Aucune réponse pour: {question_text}")
        return
    
    print(f"\n📊 {question_text}")
    counts = Counter(all_choices)
    
    for choice, count in counts.most_common():
        pct = (count / len(responses)) * 100
        bar = "█" * int(pct / 3)
        print(f"   • {choice:<30}: {count:2d} ({pct:5.1f}%) {bar}")

def analyze_open_questions(responses, key, question_text):
    """Affiche les réponses ouvertes"""
    print(f"\n💭 {question_text}")
    print("=" * 80)
    
    answers = [r[key] for r in responses if key in r and r[key]]
    
    if not answers:
        print("   Aucune réponse")
        return
    
    for i, answer in enumerate(answers, 1):
        print(f"\n{i}. {answer}")
    
    print("\n" + "=" * 80)

def generate_report(responses):
    """Génère le rapport complet d'analyse"""
    print("="*80)
    print("📊 ANALYSE DES FEEDBACKS TP OREI")
    print("="*80)
    print(f"\nNombre total de réponses: {len(responses)}")
    
    # Emails uniques
    emails = [r['email'] for r in responses if 'email' in r]
    print(f"Emails uniques: {len(set(emails))}")
    
    if len(set(emails)) != len(emails):
        print("⚠️ ATTENTION: Doublons détectés!")
    
    print("\n" + "="*80)
    print("ORGANISATION DU TP")
    print("="*80)
    
    analyze_scale_question(responses, 'clarte_consignes', 
                          "Clarté des consignes (1-5)")
    analyze_choice_question(responses, 'duree', 
                           "Durée du TP")
    analyze_scale_question(responses, 'materiel', 
                          "Qualité du matériel (1-5)")
    
    print("\n" + "="*80)
    print("OBJECTIFS PÉDAGOGIQUES")
    print("="*80)
    
    analyze_choice_question(responses, 'objectifs', 
                           "Compréhension des objectifs")
    analyze_multiselect(responses, 'competences', 
                       "Compétences développées")
    
    print("\n" + "="*80)
    print("TRAVAIL EN ÉQUIPE")
    print("="*80)
    
    analyze_choice_question(responses, 'taille', 
                           "Taille des équipes")
    analyze_scale_question(responses, 'collaboration', 
                          "Qualité de la collaboration (1-5)")
    
    print("\n" + "="*80)
    print("ÉVALUATION")
    print("="*80)
    
    analyze_scale_question(responses, 'criteres', 
                          "Clarté des critères d'évaluation (1-5)")
    analyze_choice_question(responses, 'charge', 
                           "Charge de travail")
    
    print("\n" + "="*80)
    print("NOTE GLOBALE")
    print("="*80)
    
    analyze_scale_question(responses, 'note', 
                          "Note globale du TP (0-10)")
    
    # Réponses ouvertes
    print("\n" + "="*80)
    print("FEEDBACKS QUALITATIFS")
    print("="*80)
    
    analyze_open_questions(responses, 'positifs', 
                          "Points positifs")
    analyze_open_questions(responses, 'ameliorer', 
                          "Points à améliorer")
    analyze_open_questions(responses, 'suggestions', 
                          "Suggestions")
    analyze_open_questions(responses, 'commentaires', 
                          "Autres commentaires")
    
    print("\n" + "="*80)
    print("✅ ANALYSE TERMINÉE")
    print("="*80)

def main():
    """Fonction principale"""
    print("\n🎯 Analyseur de Feedbacks TP OREI\n")
    
    # Créer le dossier responses s'il n'existe pas
    Path("./responses").mkdir(exist_ok=True)
    
    # Charger les réponses
    responses = load_responses("./responses")
    
    if not responses:
        print("\n📝 Instructions:")
        print("1. Créez un dossier 'responses' à côté de ce script")
        print("2. Mettez tous les fichiers JSON dedans")
        print("3. Relancez ce script")
        return
    
    # Générer le rapport
    generate_report(responses)
    
    # Sauvegarder le rapport
    # (optionnel: rediriger la sortie vers un fichier)

if __name__ == "__main__":
    main()
