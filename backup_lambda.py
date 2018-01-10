import boto3

#name of instance, local profile of aws-cli (you can use iam rolem just remove profile options everywhere), volume of instance, count - how many backups need to keep
def create_snapshots(name, profile, region ,volume, count):

	session = boto3.Session(profile_name = profile, region_name = region)

	ec2_client = session.resource('ec2')
	volume = ec2_client.Volume(volume)

	snapshot = volume.create_snapshot()
	ec2_client.Snapshot(snapshot.id).create_tags(Tags=[{'Key': 'Name','Value': name}])

	snapshots_list = list()
	for x in volume.snapshots.all():
		print(x.id,' ', ec2_client.Snapshot(x.id).start_time)
		snapshots_list.append([x.id, ec2_client.Snapshot(x.id).start_time])
	#print()

	snapshots_list=sorted(snapshots_list, key=lambda date: date[1])
	k=len(snapshots_list)
	while k>count:
		item=snapshots_list[0]

		#print(k, item[0])
		try:
			ec2_client.Snapshot(item[0]).delete()
		except Exception as e:
			print("Error:", str(e))

		del snapshots_list[0]
		k=len(snapshots_list)


	return

create_snapshots('instance1', 'profile1', 'us-east-1', 'vol-xxxxxxxx', 16)
create_snapshots('instance2', 'profile2', 'eu-central-1', 'vol-xxxxxxxxxxx', 7)


