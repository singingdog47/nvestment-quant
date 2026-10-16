from horizon_outlook import run


if __name__ == "__main__":
    result = run()
    for name, path in result.items():
        print(f"{name}={path}")
