from modules.onboarding.service.onboarding_service import OnboardingService

onboardingService = OnboardingService()


def test_remove_onboarding(client, api_key):
    response = client.put(
        "/onboarding",
        headers={"Authorization": "Bearer " + api_key},
        json={
            "onboarding_a": False,
            "onboarding_b1": False,
            "onboarding_b2": False,
            "onboarding_b3": False,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User onboarding not updated"}


def test_create_onboarding(client, api_key):
    response = client.get("/user", headers={"Authorization": "Bearer " + api_key})

    create_user_onboarding_response = onboardingService.create_user_onboarding(
        response.json().get("id")
    )
    assert create_user_onboarding_response == {
        "onboarding_a": True,
        "onboarding_b1": True,
        "onboarding_b2": True,
        "onboarding_b3": True,
    }


def test_get_onboarding(client, api_key):
    response = client.get(
        "/onboarding",
        headers={"Authorization": "Bearer " + api_key},
    )
    assert response.status_code == 200
    assert "onboarding_a" in response.json()
    assert "onboarding_b1" in response.json()
    assert "onboarding_b2" in response.json()
    assert "onboarding_b3" in response.json()


def test_update_onboarding_to_false(client, api_key):
    response = client.put(
        "/onboarding",
        headers={"Authorization": "Bearer " + api_key},
        json={
            "onboarding_a": False,
            "onboarding_b1": False,
            "onboarding_b2": False,
            "onboarding_b3": False,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "onboarding_a": False,
        "onboarding_b1": False,
        "onboarding_b2": False,
        "onboarding_b3": False,
    }


def test_onboarding_empty(client, api_key):
    response = client.get(
        "/onboarding",
        headers={"Authorization": "Bearer " + api_key},
    )
    assert response.status_code == 200
    assert response.json() == None
