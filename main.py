from controllers import rpc_calls, auth

def main():
    # dummy profile
    profile = auth.create_profile(1, "8728670", "password")
    print(profile)

    # dummy call check
    response = rpc_calls.get_attendance(2)
    if response is None:
        print("Error")
    
    print(response)

if __name__ == "__main__":
    main()