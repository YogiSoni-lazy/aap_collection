# List available SSH roles
path "ssh-client-signer/roles/*" {
 capabilities = ["list"]
}

# Allow SSH client signer access to devops role
path "ssh-client-signer/sign/devops" {
 capabilities = ["create","update"]
}
