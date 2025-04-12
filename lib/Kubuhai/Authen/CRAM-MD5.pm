use KubuHai::Authen::CRAM_MD5;

# Initialize CRAM-MD5 authentication
my $auth = KubuHai::Authen::CRAM_MD5->new(
    mechanism => 'CRAM-MD5',
    callback  => {
        user => 'testuser',
        pass => 'password123',
    },
);

# Start the authentication process
my $start_response = $auth->client_start();

# Assume $challenge comes from the server
my $challenge = "server-challenge-string";
my $response = $auth->client_step($challenge);

print "Authentication response: $response\n";
