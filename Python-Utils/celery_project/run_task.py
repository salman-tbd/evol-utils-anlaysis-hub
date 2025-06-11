from tasks import greet

if __name__ == "__main__":
    result = greet.delay("Salman")
    print("Task sent! Waiting for result...")
    print("Result:", result.get(timeout=10))
