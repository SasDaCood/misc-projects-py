from PIL import Image
from time import sleep
from decimal import Decimal,getcontext


missing_file_responses = (
	"Woops haha, you must've accidentally replaced the ali.jpg file that came with the program!\nI'm a nice guy, so I'll wait while you go fix that up.\nPress enter the continue, my friend! After all, this is your (belated) birthday gift.",
	"Haha... you must've forgotten, dear friend!\nI told you to go and find me a new ali.jpg file.\nCome now, we don't have all day! :)",
	"Friend, mistakes happen, but my patience wears thin...\nWould you please, for your own sake,\nget me th3 k0rrecT aaLI.jePg",
	"1 wI11 Rip 0UT yoUr 3ntr@il5   co0K 1hEM W1tH mY 501d3r1NG 1R0n   @nd f3ed tH3m t0 tHE <3-cr@ft1an h0rR0r KnoWN A5 "
)

glitch_text = ("Sas", "SAS", "5AS", "Sa5", "5A5", "S/5", "5@S", "5@5", "DQX", "QdG", "n7f", "hCe", "KOZ", "1wt", "[REDACTED]")

WIDTH,HEIGHT = 107,17
FOO = 17
getcontext().prec = 600


def check_px(x,y):
	powered = 2 ** Decimal(-FOO * int(x) - int(y)%FOO)
	return int(( y//FOO * powered )%2) > 0.5


print("Happy birthday, dear friend! Welcome to the Everything Equation!\nPress enter to try and graph the given image!\nNote: please don't remove the ali.jpg that you got with this program! :)")

for looped in range(5):
	try:
		input()
		og_img = Image.open("ali.jpg").convert("1")
		if og_img.size != (WIDTH,HEIGHT): raise FileNotFoundError
		break
	except FileNotFoundError:
		if looped == 3:
			print(missing_file_responses[looped], end="", flush=True)
			sleep(0.25)
			delay = 1.5

			for text in glitch_text:		# this whole loop should take just around 6 seconds
				print(text, end="", flush=True)
				sleep(delay)
				print("\b\b\b", end="", flush=True)
				delay /= 1.3

			sleep(1)
			print("\b\b\bPress enter to continue... ", end="", flush=True)
			sleep(0.5)
			print("and don't make a mistake this time, friend.")

		elif looped == 4:
			for i in range(3):
				print(". ", end="", flush=True)
				sleep(0.75)
		else:
			print(missing_file_responses[looped])
else:
	file = open("fuck u.txt","w+")
	file.write("fuck u")
	file.close()	# fuck u

	fuck_u = "fuck u"
	while 1:
		print(fuck_u, end="  ")
		fuck_u = f"{fuck_u} {fuck_u}"

pix = og_img.load()
bin_list = []
for x in range(WIDTH):
	for y in range(HEIGHT-1, -1, -1):
		bin_list.append(int(not bool(pix[x,y])))
k = int("".join(map(str, bin_list)), 2) * 17


print(f"k is... {k}.\n\nHuge number, innit?")


img = Image.new("1", (WIDTH+10,HEIGHT+10), 255)		# graph is from (k+17)+5 to k-5 on the y axis, -5 to (WIDTH+5)-1 on the x axis 
print("Graphing the thingo...")

x = 0
for graph_x in range(WIDTH+4, -6, -1):
	y = img.height - 1

	for graph_y in range(k+22, k-6, -1):
		#print(f"now at {graph_x},{graph_y-k}")
		if check_px(graph_x,graph_y):  img.putpixel((x,y), 0)

		y -= 1

	x += 1

print("Aight, it's done! Displaying...")
img.show("nice ALI man")

input("Press enter to continue")
img.save("ali.png")
