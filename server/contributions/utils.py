from server.models import Contribution


def create_contribution(data):
    response = data['response']
    if not data['response']:
        return None
    identity_type = response.get('identity_type')
    depict_accuracy=response.get('depict_accuracy')
    subject_relevance=response.get('subject_relevance')
    region_alt=response.get('region_alt')
    region=response.get('region')
    representation=response.get('representation')
    username = data.get('username', 'Anonymous')

    contribution = Contribution(
        filename=data['filename'],
        type=data['track'],
        identity_type=identity_type,
        depict_accuracy=depict_accuracy,
        subject_relevance=subject_relevance,
        region_alt=region_alt,
        region=region,
        representation=representation,
        username=username
    )

    return contribution
