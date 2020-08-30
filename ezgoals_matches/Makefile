SERVICE=EzGoalsMatches

build:
	sam build -m requirements.txt --use-container

run:
	sam local invoke "$(SERVICE)" -e events/basic.json 

zip:
	../zip.bash $(SERVICE)
	cp .aws-sam/package/$(SERVICE).zip .

clean:
	rm -rf .aws-sam