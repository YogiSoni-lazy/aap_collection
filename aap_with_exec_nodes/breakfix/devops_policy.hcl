# List available SSH roles
path "ssh-client-signer/roles/*" {
 capabilities = ["list"]
}

# Allow access to SSH role
path "ssh-client-signer/sign/devops-role" {
 capabilities = ["create","update"]
}
