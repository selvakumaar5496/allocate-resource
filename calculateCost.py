from flask import Flask,jsonify,request
#from flask_cors import CORS
import json

unit = {'Large' : 10,
        'XLarge' : 20,
        '2XLarge' : 40,
        '4XLarge' : 80,
        '8XLarge' : 160,
        '10XLarge' : 320}

cost = {'New york' : [120, 230, 450, 774, 1400, 2820],
        'India' : [140, 0, 413, 890, 1300, 2970],
        'China' : [110, 200, 0, 670, 1180, 0]
        }

app = Flask(__name__)
#CORS(app)
@app.route('/')
def start():
    return 'Flask service for cost calculation is up'
@app.route('/calculateMinimumCost', methods=['POST'])
def allocateResource():
    try:
        hours = request.json['hours']
        capacity = request.json['capacity']
        if capacity%10 != 0:
            return jsonify({'Constraints' : 'Please specify capacity in multiples of 10'})
        output = index = []
        for k, v in cost.items():
            l = list(unit.values())
            m = list(unit.keys())
            q = 0
            d = {}
            e = {}
            d["region"] = k
            if 0 in v:
                index = [ind for ind in range(0,len(v)) if v[ind] == 0]
            for i in range(len(l)):
                    machines = []
                    Total_sum =0     
                    i = len(l)-i-1
                    r = capacity
                    while True:
                        if i not in index:
                            q, r = divmod(r, l[i])
                            if q!=0:
                                machines.append((m[i], q))
                            s = (q*v[i]*hours)
                        Total_sum += s
                        i -= 1
                        if i == -1:
                            break
                    e[Total_sum] = machines
            d["total_cost"] = min(e.keys())
            d["machines"] = e[d["total_cost"]]
                    # print("Total : " +str(Total_sum))
            output.append(d)
        return jsonify({'op' : output})
    except Exception as ex:
        return jsonify({'Exception' : str(ex)})
    
if __name__ == '__main__':
    app.run('0.0.0.0')
