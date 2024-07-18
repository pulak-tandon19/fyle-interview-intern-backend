import json


def test_student_api_without_student_id(client):
    response = client.get(
        "/student/assignments",
        headers={"X-Principal": json.dumps({"user_id": 3})},
    )
    assert response.status_code == 403
    assert response.json["message"] == "requester should be a student"


def test_student_api_without_student_id(client):
    response = client.get(
        "/student/assignments",
        headers={"X-Principal": json.dumps({"user_id": 3})},
    )
    assert response.status_code == 403
    assert response.json["message"] == "requester should be a student"


def test_teacher_api_without_teacher_id(client):
    response = client.get(
        "/teacher/assignments",
        headers={"X-Principal": json.dumps({"user_id": 3})},
    )
    assert response.status_code == 403
    assert response.json["message"] == "requester should be a teacher"


def test_principal_api_without_principal_id(client):
    response = client.get(
        "/principal/assignments",
        headers={"X-Principal": json.dumps({"user_id": 3})},
    )
    assert response.status_code == 403
    assert response.json["message"] == "requester should be a principal"
