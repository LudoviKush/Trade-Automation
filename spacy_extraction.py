import spacy

# Load the multi-language model
nlp = spacy.load("xx_ent_wiki_sm")

nlp.add_pipe('sentencizer')

def trade_details_extraction(text_message):
    # Process the text with spaCy
    doc = nlp(text_message)

    # Initialize a dictionary to hold the extracted information
    extracted_info = {
        'management': None,
        'couple': None,
        'ote': None,
        'target_5': None,
        'stop_loss': None,
        'side': None
    }

    # Iterate over the sentences to find the relevant information
    for sent in doc.sents:
        text = sent.text.strip()
        if 'Direzione:' in text:
            direction = text.split('Direzione:')[-1].strip()
            extracted_info['management'] = 'LONG' if 'LONG' in direction else 'SHORT'
        
        if 'Coppia:' in text:
            pair = text.split('Coppia:')[-1].split()[0].strip()
            extracted_info['couple'] = pair.replace('/', '').upper().replace('$', '')
        
        if '(OTE:' in text:
            ote = text.split('(OTE:')[-1].split(')')[0].strip()
            extracted_info['ote'] = ote.replace(',', '.')
        
        if 'Target 5 -' in text:
            target_5 = text.split('Target 5 -')[-1].split('\n')[0].strip()  # Split and take the first part before a newline
            extracted_info['target_5'] = target_5
        
        if 'STOP LOSS:' in text:
            stop_loss = text.split('STOP LOSS:')[-1].split('\n')[0].strip()  # Split and take the first part before a newline
            extracted_info['stop_loss'] = stop_loss.replace(',', '.')

    # Determine the side based on the management value
    extracted_info['side'] = "Buy" if extracted_info['management'] == "LONG" else "Sell"

    return extracted_info