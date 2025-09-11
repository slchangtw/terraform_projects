import subprocess


def get_terraform_output(output_name: str) -> str:
    """Get a specific Terraform output value"""
    try:
        result = subprocess.run(
            ["terraform", "output", "-raw", output_name],
            cwd="terraform",
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting Terraform output '{output_name}': {e}")
        return None


def get_api_gateway_url():
    """Get the API Gateway URL from the Terraform outputs"""
    try:
        return get_terraform_output("api_gateway_url")
    except Exception as e:
        print(f"Error getting API Gateway URL: {e}")
        return None
