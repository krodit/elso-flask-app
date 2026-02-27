from flask import Flask, render_template_string, request, Response
import io, csv

app = Flask(__name__)

# HTML sablon (egy fájlban a Python kóddal a könnyebbség kedvéért)
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Python Lottó Ellenőrző</title>
    <style>
        body { font-family: sans-serif; margin: 40px; background: #f4f4f4; }
        .box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        input { margin-bottom: 10px; }
        button { background: #27ae60; color: white; border: none; padding: 10px 20px; cursor: pointer; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background: #34495e; color: white; }
        .win { background: #fff3e0; font-weight: bold; }
    </style>
</head>
<body>
    <div class="box">
        <h2>Hatoslottó Ellenőrző (Python + Flask)</h2>
        <form method="post" enctype="multipart/form-data">
            <label>Húzások (14 szám):</label><br><input type="file" name="huzasok"><br>
            <label>Variációk (7 szám):</label><br><input type="file" name="variaciok"><br><br>
            <button type="submit">Elemzés indítása</button>
        </form>

        {% if stats %}
        <h3>Statisztika</h3>
        <table>
            <tr><th>Találat</th><th>Gépi</th><th>Kézi</th></tr>
            {% for i in range(7, -1, -1) %}
            <tr><td>{{i}} találat</td><td>{{stats['gepi'][i]}}</td><td>{{stats['kezi'][i]}}</td></tr>
            {% endfor %}
        </table>

        <h3>Nyertesek (4+)</h3>
        {% if nyertesek %}
        <table>
            <tr><th>Év/Hét</th><th>Típus</th><th>Találat</th><th>Számaid</th></tr>
            {% for n in nyertesek %}
            <tr class="win"><td>{{n[0]}}/{{n[1]}}</td><td>{{n[2]}}</td><td>{{n[3]}}</td><td>{{n[4]}}</td></tr>
            {% endfor %}
        </table>
        {% else %}<p>Nincs 4+ találat.</p>{% endif %}
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    stats = None
    nyertesek = []
    
    if request.method == 'POST':
        h_file = request.files['huzasok'].read().decode('utf-8').splitlines()
        v_file = request.files['variaciok'].read().decode('utf-8').splitlines()
        
        stats = {"kezi": [0]*8, "gepi": [0]*8}
        variaciok = [line.replace(';', ',').split(',') for line in v_file if len(line.strip()) > 5]
        variaciok = [[n.strip() for n in v if n.strip()] for v in variaciok]

        for line in h_file:
            p = [x.strip() for x in line.split(';') if x.strip()]
            if len(p) < 14: continue
            
            ev, het = p[0], p[1]
            nums = p[-14:]
            g_huzas = set(nums[:7])
            k_huzas = set(nums[7:])

            for var in variaciok:
                if len(var) != 7: continue
                v_set = set(var)
                g_c, k_c = len(v_set & g_huzas), len(v_set & k_huzas)
                
                stats["gepi"][g_c] += 1
                stats["kezi"][k_c] += 1
                
                if g_c >= 4: nyertesek.append([ev, het, "Gépi", g_c, ",".join(var)])
                if k_c >= 4: nyertesek.append([ev, het, "Kézi", k_c, ",".join(var)])

    return render_template_string(HTML_PAGE, stats=stats, nyertesek=nyertesek)

if __name__ == '__main__':
    app.run(debug=True)
