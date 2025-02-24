PROMPTS_SEND_EMAIL = {
    "email_reply": """Tu dois répondre au mail de {sender_email} avec le sujet '{subject}' et le message suivant :
    
    ---
    {email_content}
    ---

    Pour cela, utilise l'outil 'send_email' et ajoute ta réponse.  
    **Instructions importantes :**
    - Réponds **en haut du mail**.
    - **Conserve** le fil de discussion tel quel.
    - **Ne reformule pas** le message précédent.
    - Commence toujours par **une réponse formelle**.
    - Insère une ligne de séparation `--- Email précédent ---` et affiche **l’email d’origine** en conservant **sa mise en forme**.
    
    Réponds uniquement en exécutant la fonction `send_email`.
    """
}