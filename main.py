import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

amount_of_people = 50
income_tax = 0.05
wealth_tax = 0.3

n = amount_of_people - 1
p = 1 / float(amount_of_people - 1)
start_money = 50

bank = start_money*np.ones([amount_of_people])

range = np.arange(amount_of_people)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

bar = plt.bar(range,bank)

def init():
    return bar

def animate(i):
    global bank, ax
    people_without_money = sum(bank==0)
    smpl_w_money = np.random.binomial(amount_of_people - 1 - people_without_money, p, amount_of_people)
    smpl_wo_money = np.random.binomial(amount_of_people - people_without_money, p, amount_of_people)
    smpl_w_money[bank == 0] = 0
    smpl_wo_money[bank > 0] = 0
    sample = smpl_w_money + smpl_wo_money
    taxed_transfer = income_tax*sample
    not_taxed_transfer = (1-income_tax)*sample - 1*(bank > 0)
    distributed_income_tax = np.sum(np.abs(taxed_transfer)) / (amount_of_people)
    taxed_wealth = wealth_tax*bank
    distributed_wealth_tax = np.sum(np.abs(taxed_wealth)) / (amount_of_people)
    bank = bank + not_taxed_transfer + distributed_income_tax - taxed_wealth + distributed_wealth_tax
    bank = np.sort(bank)
    for rect, y in zip(bar, bank):
        rect.set_height(y)
    ax.set_ylim(0,max(bank))
    ax.set_title(i)
    #print(sum(bank)/amount_of_people)
    return bar

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=3000, interval=1, blit=False)

anim.save('basic_animation_high_wealth_low_income_tax.mp4', fps=60, extra_args=['-vcodec', 'libx264'])

plt.show()
