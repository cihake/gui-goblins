from django.db import models

Class CommunityChestCards(models.Model)
	description = models.CharField(max_length=100, null=True)

Class ChanceCards(models.Model)
	description = models.CharField(max_length=100, null=True)

	community_chest_card = CommunityChestCards(description="Your description here")
	community_chest_card.save()

	chance_card = ChanceCards(description="Your description here")
	chance_card.save()