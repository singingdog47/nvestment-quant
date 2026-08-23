from final_report import build_final_report


def main() -> None:
    public_path, private_path = build_final_report('.')
    print(f'public_report={public_path}')
    print(f'private_report_generated={private_path is not None}')


if __name__ == '__main__':
    main()
