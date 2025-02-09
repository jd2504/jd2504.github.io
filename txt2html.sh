#!/bin/bash


if [ $# -ne 1 ]; then
    echo "Usage: $0 <input_file.txt>"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Error: File '$1' not found"
    exit 1
fi

input_file="$1"
output_file="${input_file%.*}.html"

input_file="$1"
output_file="${input_file%.*}.html"


cat > "$output_file" << HTML_HEADER
cat > "$output_file" << HTML_HEADER
<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-RWPLPJ3ZCL"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-RWPLPJ3ZCL');
    </script>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>${input_file%.*}</title>
 <style>
     body {
         font-family: Arial, sans-serif;
         line-height: 1.6;
         margin: 40px;
     }
     p {
         margin-bottom: 1em;
     }
 </style>
</head>
<body>
HTML_HEADER


while IFS= read -r line; do
    if [ -z "$line" ]; then
	echo "<br>" >> "$output_file"

    else
	line=$(echo "$line" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g; s/"/\&quot;/g; s/'"'"'/\&#39;/g')
	echo "<p>$line</p>" >> "$output_file"

    fi
done < "$input_file"

cat >> "$output_file" << HTML_FOOTER
</body>
</html>
HTML_FOOTER

echo "Output HTML saved as: $output_file"
