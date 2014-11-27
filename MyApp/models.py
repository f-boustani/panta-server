from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
	
task_CHOICES =(
	('1','Doing'),
	('2','Done by user'),
        ('3','accept by manager'),
)

class Login(models.Model):

    username = models.EmailField()
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=50)

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

    def as_json(self):
            return dict(
                username=self.username,
                projectID=self.projectID)
class Projects(models.Model):
    projectID = models.IntegerField(max_length=15)
    projectName = models.CharField(max_length=50)
    managerName = models.CharField(max_length=50)
    managerUser = models.EmailField()
    project_info = models.CharField(max_length=5000)
    progress = models.IntegerField(max_length=15)
    pDeadline = models.DateField()

    def as_json(self):
            return dict(
                managerName=self.managerName,
                managerUser=self.managerUser,
                projectName=self.projectName,
                projectID=self.projectID,
                project_info=self.project_info,
                progress=self.progress,
            	pDeadline=self.pDeadline)


class Task(models.Model):
    taskID = models.IntegerField(max_length=15)
    taskName = models.CharField(max_length=100) 
    task_info = models.CharField(max_length=5000)
    username = models.EmailField()
    projectID = models.IntegerField(max_length=15)
    deadline = models.DateField(null=True)
    status = models.CharField(max_length=1, choices=task_CHOICES)

    class Meta:
        unique_together = ('taskID','username')

    def as_json(self):
            return dict(
                taskID=self.taskID,
                taskName=self.taskName,
                task_info=self.task_info,
                username=self.username,
                deadline=self.deadline,
                projectID=self.projectID,
                status=self.status)


class User_father(models.Model):
    username = models.EmailField()
    projectID = models.IntegerField(max_length=15)
    father = models.EmailField()
    position = models.CharField(max_length=50)
    deadline = models.DateField(null=True)
    
    def as_json(self):
            return dict(
                projectID=self.projectID,
                father=self.father,
                username=self.username,
                position=self.position,
                deadline=self.deadline)



