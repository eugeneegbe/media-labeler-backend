import sys
import traceback

from server import db


def commit_changes_to_db():
    """
    Test for the success of a database commit operation.

    """
    try:
        db.session.commit()
        return True
    except Exception as e:
        # TODO: We could add a try catch here for the error
        print('Exception when committing to database.', file=sys.stderr)
        traceback.print_stack()
        traceback.print_exc()
        db.session.rollback()
        # for resetting non-commited .add()
        db.session.flush()
        return False


def get_serialized_data(data):
    return [datum.serialize() for datum in data]