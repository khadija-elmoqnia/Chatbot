import yaml

def load_schedule(file_path):
    with open(file_path, 'r') as file:
        schedule = yaml.safe_load(file)
    return schedule

def replace_placeholders(template, replacements):
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template

def find_matching_response(question, schedule):
    for entry in schedule:
        if 'question' in entry and entry['question'].lower() in question.lower():
            # Remplacer les placeholders avec les informations du docteur spécifique
            replacements = {
                "[Nom]": entry['nom'] if 'nom' in entry else '',
                "[Numéro de téléphone]": entry['numero_telephone'] if 'numero_telephone' in entry else '',
                "[Liste des créneaux]": ', '.join(entry['dates_disponibles']) if 'dates_disponibles' in entry else '',
                "[Liste des dates]": ', '.join(entry['dates_disponibles']) if 'dates_disponibles' in entry else '',
                "[Liste des jours]": ', '.join(entry['dates_disponibles']) if 'dates_disponibles' in entry else ''
            }
            return replace_placeholders(entry['reponse'], replacements)
    return "Je suis désolé, je n'ai pas d'informations disponibles pour cette question."