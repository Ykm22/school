-- Prosody XMPP Server Configuration for Pac-Man MAS

-- Server settings
daemonize = false
pidfile = "/var/run/prosody/prosody.pid"

-- Logging
log = {
	info = "/var/log/prosody/prosody.log",
	error = "/var/log/prosody/prosody.err",
	"*syslog",
}

-- Network settings
interfaces = { "*" }
c2s_ports = { 5222 }
c2s_ssl_ports = {}

-- Authentication
authentication = "internal_hashed"
allow_registration = true

-- SSL/TLS (disabled for local development)
ssl = {
	key = "/etc/prosody/certs/localhost.key",
	certificate = "/etc/prosody/certs/localhost.crt",
}

-- Virtual hosts
VirtualHost("localhost")
enabled = true

-- Admins
admins = { "admin@localhost" }

-- Modules
modules_enabled = {
	-- Generally required
	"roster",
	"saslauth",
	"tls",
	"dialback",
	"disco",
	"carbons",
	"pep",
	"private",
	"blocklist",
	"vcard4",
	"vcard_legacy",
	"limits",
	"version",
	"uptime",
	"time",
	"ping",
	"register",
	"admin_adhoc",
}

-- Allow unencrypted connections (for local development)
c2s_require_encryption = false
s2s_require_encryption = false
allow_unencrypted_plain_auth = true
