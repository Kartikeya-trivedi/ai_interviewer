"""Example usage of the AI Interview Platform API."""
import asyncio
import httpx
import json


async def run_example_interview():
    """Example interview flow."""
    base_url = "http://localhost:8000/api/v1"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Create interview
        print("Creating interview...")
        create_response = await client.post(
            f"{base_url}/interviews",
            json={
                "candidate_name": "Alice Smith",
                "theory_topic": "bias-variance tradeoff",
                "interview_type": "ml_junior"
            }
        )
        create_response.raise_for_status()
        interview_data = create_response.json()
        interview_id = interview_data["interview_id"]
        
        print(f"Interview created: {interview_id}")
        print(f"Interviewer: {interview_data['interviewer_response']['speech']}\n")
        
        # 2. Candidate responds
        candidate_responses = [
            "Overfitting happens when a model memorizes the training data too well and performs poorly on new data.",
            "It occurs because the model becomes too complex and captures noise in the training set.",
            "Regularization helps by adding constraints to prevent the model from becoming too complex."
        ]
        
        for i, response in enumerate(candidate_responses, 1):
            print(f"Candidate Response {i}: {response}")
            
            submit_response = await client.post(
                f"{base_url}/interviews/{interview_id}/respond",
                json={"message": response}
            )
            submit_response.raise_for_status()
            interviewer_data = submit_response.json()
            
            print(f"Interviewer: {interviewer_data['speech']}")
            print(f"Phase: {interviewer_data['meta']['phase']}")
            print(f"End Theory Round: {interviewer_data['meta']['end_theory_round']}\n")
            
            if interviewer_data['meta']['end_theory_round']:
                print("Theory round completed!")
                break
        
        # 3. Get final state
        state_response = await client.get(f"{base_url}/interviews/{interview_id}")
        state_response.raise_for_status()
        state = state_response.json()
        
        print("\nFinal Interview State:")
        print(json.dumps(state, indent=2, default=str))


if __name__ == "__main__":
    print("AI Interview Platform - Example Usage")
    print("=" * 50)
    print("Make sure the server is running: uvicorn app.main:app --reload\n")
    
    try:
        asyncio.run(run_example_interview())
    except httpx.HTTPError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

