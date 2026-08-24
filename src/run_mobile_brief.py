from mobile_brief import build_mobile_brief


def main() -> None:
    public_path, private_path = build_mobile_brief(".")
    print(f"public_mobile_brief={public_path}")
    print(f"private_mobile_brief_generated={private_path is not None}")


if __name__ == "__main__":
    main()
