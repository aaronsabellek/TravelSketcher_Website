import pytest

from app.models import Activity
from tests.helpers.functions import request_and_validate
from tests.helpers.variables import dest_main_id
from tests.test_data.activity_data import (
    new_activity,
    add_activity,
    get_all,
    get_activity,
    edit_link,
    edit_note,
    edit_activity,
    reorder_activities,
    delete_activity
)


@pytest.mark.parametrize('test_data', add_activity)
def test_add(setup_logged_in_user, test_data):
    """Test: Add activity to database"""

    # Use and validate route
    response = request_and_validate(setup_logged_in_user, f'activity/add/{test_data['destination_id']}', test_data)
    if response.status_code not in [200, 201]:
        return

    # Check for destination in db
    activity = Activity.query.filter_by(title=test_data['title']).first()
    assert activity is not None, f'Error: Activity not found in db'
    assert activity.id == new_activity['id'], f'Error: ID expected: {new_activity['id']}, but got: {activity.id}'
    assert activity.position == 6, f'Error: Position expected: 6, but got: {activity.position}'
    assert activity.destination_id == dest_main_id, f'Error: Destination-ID expected: {dest_main_id}, but got: {activity.destination_id}'


@pytest.mark.parametrize('test_data', get_all)
def test_get_all(setup_logged_in_user, test_data):
    """Test: Get all activities from specific destination"""

    # Use and validate route
    response = request_and_validate(setup_logged_in_user, f'activity/get_all/{test_data['destination_id']}', test_data, method='GET')
    if response.status_code not in [200, 201]:
        return

    # Check for correct entry
    if test_data['destination_id'] == dest_main_id:
        assert response.json['activities'][2]['title'] == 'Notre-Dame Cathedral', f'Unexpected Error: Title not found!'


@pytest.mark.parametrize('test_data', get_activity)
def test_get_destination(setup_logged_in_user, test_data):
    """Test: Get specific activity"""

    # Use route
    request_and_validate(client=setup_logged_in_user, endpoint=f'activity/get/{test_data['activity_id']}', test_data=test_data, method='GET')


# Test edit activity
@pytest.mark.parametrize('test_data', edit_activity)
def test_edit_activity(setup_logged_in_user, test_data):
    """Test: Edit activity"""

    # Use and validate route
    response = request_and_validate(setup_logged_in_user, f'activity/edit/{test_data['id']}', test_data)
    if response.status_code not in [200, 201]:
        return

    # Check for updates in db
    activity = Activity.query.filter_by(id=test_data['id']).first()
    assert activity.title == test_data['title'], f'Unexpedted Error: Activity not edited in db'


@pytest.mark.parametrize('test_data', edit_note)
def test_edit(setup_logged_in_user, test_data):
    """Test: Edit note"""

    # Use and validate route
    response = request_and_validate(setup_logged_in_user, f'activity/edit_notes/{test_data['id']}', test_data)
    if response.status_code not in [200, 201]:
        return

    # Check is note is edited in database
    activity = Activity.query.filter_by(id=test_data['id']).first()
    assert activity.free_text == test_data['free_text'], 'Activitiy is not updated correctly in database'


@pytest.mark.parametrize('test_data', edit_link)
def test_edit(setup_logged_in_user, test_data):
    """Test: Edit note"""

    # Use and validate route
    response = request_and_validate(setup_logged_in_user, f'activity/edit_link/{test_data['id']}', test_data)
    if response.status_code not in [200, 201]:
        return

    # Check is note is edited in database
    activity = Activity.query.filter_by(id=test_data['id']).first()
    assert activity.web_link == test_data['web_link'], 'Activitiy is not updated correctly in database'


@pytest.mark.parametrize('test_data', reorder_activities)
def test_edit_activity(setup_logged_in_user, test_data):
    """Test: Reorder activities of specific destination"""

    # Use and validate route
    response = request_and_validate(setup_logged_in_user, f'activity/reorder/{test_data['destination_id']}', test_data)
    if response.status_code not in [200, 201]:
        return

    # Check for new order in db
    reordered_activities = Activity.query.filter_by(destination_id=test_data['destination_id']).order_by(Activity.position).all()
    reordered_ids = [act.id for act in reordered_activities]
    assert reordered_ids == test_data['new_order'], f'Error! Expected: {test_data['new_order']}, but got: {reordered_ids}'


@pytest.mark.parametrize('test_data', delete_activity)
def test_delete(setup_logged_in_user, test_data):
    """Test: Delete activity from database"""

    # Use and validate route
    response = request_and_validate(setup_logged_in_user, f'activity/delete/{test_data['activity_id']}', test_data, method='DELETE')
    if response.status_code not in [200, 201]:
        return

    # Check if destination got deleted in db
    activity = Activity.query.filter_by(id=test_data['activity_id']).first()
    assert activity is None, f'Error: Activity still found in database'

