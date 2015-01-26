from django.db import models


	
task_CHOICES =(
	('0','Doing'),
	('1','Done by user'),
    ('2','accept by manager'),
)

notif_CHOICES =(
    ('0','not sent'),
    ('1','sent'),
)

class Gcm_users(models.Model):

    username = models.EmailField(max_length=70)
    reg_id = models.TextField()
    #class Meta:
     #  unique_together = ('username','reg_id',)
        #managed=False
    

class Notification(models.Model):

    username = models.EmailField(max_length=70)
    message = models.CharField(max_length=200)
    msg_type= models.CharField(max_length=1)
    class Meta:
        #managed=False
    def as_json(self):
            return dict(
                username=self.username,
                message=self.message,
                msg_type=self.msg_type)
                
    

        
class Login(models.Model):

    username = models.EmailField()
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        #managed=False    

    def as_json(self):
            return dict(
                username=self.username,
                password=self.password,
                name=self.name)
    

class Profile(models.Model):
    username = models.EmailField()
    projectID = models.IntegerField(max_length=15)

    class Meta:
        unique_together = ('username','projectID')
       # managed=False

    def as_json(self):
            return dict(
                username=self.username,
                projectID=self.projectID)
class Projects(models.Model):
    
    projectName = models.CharField(max_length=50)
    managerName = models.CharField(max_length=50)
    managerUser = models.EmailField()
    project_info = models.CharField(max_length=5000)
    progress = models.IntegerField(max_length=15)
    pDeadline = models.DateField()
    pDelta = models.IntegerField(max_length=15)
    link = models.TextField(null=True, blank=True)
    notif = models.CharField(max_length=1, choices=notif_CHOICES)

    #class Meta:
     #   managed=False   

    def as_json(self):
            return dict(
                managerName=self.managerName,
                managerUser=self.managerUser,
                projectName=self.projectName,
                projectID=self.id,
                project_info=self.project_info,
                progress=self.progress,
                link=self.link,
            	pDeadline=self.pDeadline)


class Task(models.Model):
    
    taskName = models.CharField(max_length=100) 
    task_info = models.CharField(max_length=5000)
    username = models.EmailField()
    projectID = models.IntegerField(max_length=15)
    deadline = models.DateTimeField(null=True)
    status = models.CharField(max_length=1, choices=task_CHOICES)
    delta = models.IntegerField(max_length=15)
    notif = models.CharField(max_length=1, choices=notif_CHOICES)

    class Meta:
        unique_together = ('id','username')
       # managed=False

    def as_json(self):
            return dict(
                taskID=self.id,
                taskName=self.taskName,
                task_info=self.task_info,
                username=self.username,
                deadline=self.deadline,
                projectID=self.projectID,
                status=self.status)


