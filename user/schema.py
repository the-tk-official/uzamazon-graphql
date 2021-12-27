import graphene
from graphene_file_upload.scalars import Upload
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery

from backend.permissions import paginate, is_authenticated
from .models import Address, UserImage
from .types import AddressType, UserImageType


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class UserImageUpload(graphene.Mutation):
    """Upload an image for user page"""
    image = graphene.Field(UserImageType)

    class Arguments:
        image = Upload(required=True)
        alt_text = graphene.String()

    @is_authenticated
    def mutate(self, info, **kwargs):
        image = UserImage.objects.filter(user_id=info.context.user.id).first()
        if image:
            image.delete()

        image = UserImage.objects.create(user=info.context.user, **kwargs)

        return UserImageUpload(image=image)


class AddressInput(graphene.InputObjectType):
    country = graphene.String()
    city = graphene.String()
    street = graphene.String()
    apartment = graphene.String()


class CreateAddress(graphene.Mutation):
    """Creating a user address"""
    address = graphene.Field(AddressType)

    class Arguments:
        address_data = AddressInput(required=True)
        is_default = graphene.Boolean()

    @is_authenticated
    def mutate(self, info, address_data, is_default=False):
        user = info.context.user

        existing_addresses = Address.objects.filter(user=user)

        if is_default:
            existing_addresses.update(is_default=False)

        address = Address.objects.create(
            user=user,
            **address_data,
            is_default=is_default
        )

        return CreateAddress(address=address)


class UpdateAddress(graphene.Mutation):
    """Updating a user address"""
    address = graphene.Field(AddressType)

    class Arguments:
        address_id = graphene.ID(required=True)
        address_data = AddressInput(required=True)
        is_default = graphene.Boolean()

    @is_authenticated
    def mutate(self, info, address_id, address_data, is_default=False):
        user = info.context.user

        Address.objects.filter(
            user=user,
            id=address_id
        ).update(**address_data, is_default=is_default)

        if is_default:
            Address.objects.filter(user=user).exclude(
                id=address_id
            ).update(
                is_default=False
            )

        return UpdateAddress(
            address=Address.objects.get(id=address_id)
        )


class DeleteAddress(graphene.Mutation):
    """Deleting a user address"""
    status = graphene.Boolean()

    class Arguments:
        address_id = graphene.ID(required=True)

    @is_authenticated
    def mutate(self, info, address_id):
        user = info.context.user

        Address.objects.filter(
            user=user,
            id=address_id
        ).delete()

        return DeleteAddress(status=True)


class Query(UserQuery, MeQuery, graphene.ObjectType):
    image_uploads = graphene.Field(paginate(UserImageType), page=graphene.Int())

    @staticmethod
    def resolve_image_uploads(info, **kwargs):
        return UserImage.objects.filter(**kwargs)


class Mutation(AuthMutation, graphene.ObjectType):
    user_image_upload = UserImageUpload.Field()
    create_address = CreateAddress.Field()
    update_address = UpdateAddress.Field()
    delete_address = DeleteAddress.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
