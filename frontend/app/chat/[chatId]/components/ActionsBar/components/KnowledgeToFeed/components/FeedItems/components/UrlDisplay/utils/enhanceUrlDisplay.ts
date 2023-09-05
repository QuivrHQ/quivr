export const enhanceUrlDisplay = (url: string): string => {
  const parts = url.split("/");

  // Check if the URL has at least 3 parts (protocol, domain, and one more segment)
  if (parts.length >= 3) {
    const domain = parts[2];
    const path = parts.slice(3).join("/");

    // Split the domain by "." to check for subdomains and remove "www"
    const domainParts = domain.split(".");
    if (domainParts[0] === "www") {
      domainParts.shift(); // Remove "www"
    }

    // Combine the beginning (subdomain/domain) and the end (trimmed path)
    const beginning = domainParts.join(".");
    const trimmedPath = path.slice(0, 5) + "..." + path.slice(-5); // Display the beginning and end of the path

    return `${beginning}/${trimmedPath}`;
  }

  // If the URL doesn't have enough parts, return it as is
  return url;
};
