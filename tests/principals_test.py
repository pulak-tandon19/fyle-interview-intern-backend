from core.models.assignments import AssignmentStateEnum, GradeEnum, Assignment
from core import db
import pytest


@pytest.fixture()
def set_assignment_to_draft():
    assignment = Assignment.get_by_id(5)
    assignment.state = AssignmentStateEnum.DRAFT
    db.session.commit()

    yield assignment


@pytest.fixture
def assignment_to_grade():
    assignment = Assignment.get_by_id(4)
    assignment.state = AssignmentStateEnum.SUBMITTED
    db.session.commit()

    yield assignment

    assignment.state = AssignmentStateEnum.DRAFT
    db.session.commit()


@pytest.fixture
def assignment_to_regrade(scope="function"):
    assignment = Assignment.get_by_id(4)
    assignment.state = AssignmentStateEnum.GRADED
    db.session.commit()

    yield assignment

    assignment.state = AssignmentStateEnum.DRAFT
    db.session.commit()


def test_get_assignments(client, h_principal):
    response = client.get("/principal/assignments", headers=h_principal)

    assert response.status_code == 200

    data = response.json["data"]
    for assignment in data:
        assert assignment["state"] in [
            AssignmentStateEnum.SUBMITTED,
            AssignmentStateEnum.GRADED,
        ]


def test_grade_assignment_draft_assignment(
    client, h_principal, set_assignment_to_draft
):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        "/principal/assignments/grade",
        json={"id": 5, "grade": GradeEnum.A.value},
        headers=h_principal,
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal, assignment_to_grade):
    response = client.post(
        "/principal/assignments/grade",
        json={"id": 4, "grade": GradeEnum.C.value},
        headers=h_principal,
    )

    assert response.status_code == 200

    assert response.json["data"]["state"] == AssignmentStateEnum.GRADED.value
    assert response.json["data"]["grade"] == GradeEnum.C


def test_regrade_assignment(client, h_principal, assignment_to_regrade):
    response = client.post(
        "/principal/assignments/grade",
        json={"id": 4, "grade": GradeEnum.B.value},
        headers=h_principal,
    )

    assert response.status_code == 200

    assert response.json["data"]["state"] == AssignmentStateEnum.GRADED.value
    assert response.json["data"]["grade"] == GradeEnum.B


def test_wrong_grade(client, h_principal, assignment_to_regrade):
    response = client.post(
        "/principal/assignments/grade",
        json={"id": 4, "grade": "z"},
        headers=h_principal,
    )

    assert response.status_code == 400
    data = response.json

    assert data["error"] == "ValidationError"


def test_principal_grade_assignment_bad_assignment(client, h_principal):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        "/principal/assignments/grade",
        headers=h_principal,
        json={"id": 100000, "grade": "A"},
    )

    assert response.status_code == 404
    data = response.json

    assert data["error"] == "FyleError"


def test_get_teachers_list(client, h_principal):
    response = client.get("/principal/teachers", headers=h_principal)
    assert response.status_code == 200
