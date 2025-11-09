class HTMLBuilder:
    @staticmethod
    def build_page(title, urls):
        html = f"""
        <html>
          <head>
            <meta charset="utf-8"/>
            <title>{title}</title>
            <style>
              body {{ font-family: Arial; margin: 30px; background: #fafafa; }}
              h2 {{ color: #0078D7; }}
              a {{ color: #0078D7; text-decoration: none; }}
              a:hover {{ text-decoration: underline; }}
              div {{ margin-bottom: 8px; }}
            </style>
          </head>
          <body>
            <h2>{title}</h2>
        """
        for u in urls:
            html += f"<div><a href='{u}' target='_blank'>{u}</a></div>\n"
        html += """
          </body>
        </html>
        """
        return html
