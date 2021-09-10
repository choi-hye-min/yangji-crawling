def createMessage(items = []):
    htmlItems = ''
    if items.__len__() == 0:
        htmlItems = """
        <tr>
              <td colspan="100" style="text-align:center;">키워드에 검색된 항목이 없습니다.</td>
        </tr>
        """

    for type, title, source, link in items:
        htmlItems += """
        <tr>
              <td style="text-align: center;">{}</td>
              <td style="text-align: left;">{}</td>
              <td style="text-align: left;">{}</td>
              <td style="text-align: left;"><a href="{}">바로가기</a></td>
        </tr>
        """.format(type, title, source, link)

    template = """\
    <!DOCTYPE html>
    <html>
          <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
          </head>
        <body style="padding: 0; margin: 0;">
            <div style="background-color:white;padding:10px 20px;text-align: center;color: black;">
                <img src="https://www.newyjh.com/images/logo-sub.gif">
                <h3 style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349;">Naver Yangji <font color="red">Keyword</font> Alert</h3>
            </div>
            <div>발견된 항목 : {}개</div>
            <table width="100%" bgcolor="black" style="color:white;">
                <tr>
                      <th style="width: 10%;">TYPE</th>
                      <th style="width: 30%;">TITLE</th>
                      <th style="width: 20%;">SOURCE</th>
                      <th style="width: 10%;">LINK</th>
                </tr>
                {}
            </table>
            
            <div style="margin-top: 10px; padding: 10px;text-align: center; border-top: 1px solid red;">
              <h3>For My Love❤ Park H.R</h3>
              <small style="color: silver;">네이버 모바일/PC에 양지병원 관련 키워드가 발생시 자동 송신되는 메일입니다.</small>
            </div>
        </body>
    </html>
    """.format(items.__len__(), htmlItems)

    return template