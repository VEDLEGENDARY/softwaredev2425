r = """
<!DOCTYPE html>
<html>

<head>

</head>

<body>
 er:feels_like_temperature}°F</p>
        <p>
        """

for segment in r.split("```"):
    if "<" in segment:
        response = segment
if response[0:4] == "html": response = response.lstrip("html").strip()
print(r)