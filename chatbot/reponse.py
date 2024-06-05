import yaml
from NLP.nlp import find_most_similar_question_nlp_combined,load_yaml,similar




def getResponse(input_question):

    yaml_file_path = 'Base de connaisance/base.yml'
    questions_and_responses = load_yaml(yaml_file_path)
    # Créez une liste contenant toutes les questions de la base YAML
    questions = [qa_pair['question'] for qa_pair in questions_and_responses]
    # Appel à la fonction find_most_similar_question_nlp_combined
    similar_question = find_most_similar_question_nlp_combined(input_question, questions)

    # Si la question similaire est None, demandez une reformulation
    if similar_question is None:
        return "Je n'ai pas compris. Pouvez-vous reformuler la question?"
    
    # Ajoutez la condition pour appeler prend_rendezvous si la question est liée à la prise de rendez-vous
    if  similar(input_question,"Je veux prendre un rendez-vous"):
        #prend_rendezvous() 
        pass
    # Récupérez la réponse associée à la question la plus similaire
    for qa_pair in questions_and_responses:
        if qa_pair['question'] == similar_question:
            return qa_pair['reponse']

