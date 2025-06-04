package DB;
use strict;
use warnings;
use DBI;
use Config::Simple;
use Exporter 'import';

our @EXPORT_OK = qw(connect_db create_tables insert_user get_user_by_username update_password);

# Load configuration
my $cfg = Config::Simple->new('config.cfg');

sub connect_db {
    my $db_name = $cfg->param('db_name');
    my $dbh = DBI->connect("dbi:SQLite:dbname=$db_name", "", "", { RaiseError => 1, AutoCommit => 1 });
    return $dbh;
}

sub create_tables {
    my $dbh = connect_db();
    $dbh->do(<<'SQL');
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            last_updated DATETIME
        );
SQL

    $dbh->do(<<'SQL');
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            username TEXT,
            created_at DATETIME,
            expires_at DATETIME
        );
SQL
}

sub insert_user {
    my ($username, $password) = @_;
    my $dbh = connect_db();
    my $sth = $dbh->prepare("INSERT INTO users (username, password, last_updated) VALUES (?, ?, datetime('now'))");
    $sth->execute($username, $password);
}

sub get_user_by_username {
    my ($username) = @_;
    my $dbh = connect_db();
    my $sth = $dbh->prepare("SELECT * FROM users WHERE username = ?");
    $sth->execute($username);
    return $sth->fetchrow_hashref();
}

sub update_password {
    my ($username, $new_password) = @_;
    my $dbh = connect_db();
    my $sth = $dbh->prepare("UPDATE users SET password = ?, last_updated = datetime('now') WHERE username = ?");
    $sth->execute($new_password, $username);
}

1;
