from models.combatant_update import CombatantUpdate, InvalidCode

from cards.models.permission import PermissionDenied


def update_info(combatant, data, code=None):
    """Update combatant combatant-serve data properties.

    Args:
        data: A dict of combatant data to update
        code: The one-time code provided to validate the update

    Raises:
        InvalidCode: If the code provided is invalid or has already been used
        InvalidData: If the data provided is invalid

    """
    if code:
        # Check if the code is valid and has not been used
        try:
            combatant_update = CombatantUpdate.objects.get(
                combatant=combatant, code=code, used=False
            )
        except CombatantUpdate.DoesNotExist:
            raise InvalidCode("The code provided is invalid or has already been used")

        # Mark the code as used
        combatant_update.used = True
        combatant_update.save()
    else:
        # Check if the user has the required permissions
        if not combatant.has_permission("write_combatant_info"):
            raise PermissionDenied("You do not have permission to perform this action")

    combatant.validate_data(data)

    # Only update the fields that are allowed to be updated by the combatant
    allowed_fields = [
        "email",
        "sca_name",
        "phone",
        "address1",
        "address2",
        "city",
        "province",
        "postal_code",
        "member_expiry",
        "member_number",
    ]
    for field in data.keys():
        if field not in allowed_fields:
            raise ValueError(f"{field} cannot be updated by the combatant")

    # Do the updates
    for field, value in data.items():
        if field in combatant._encrypt_info:
            combatant.decrypted[field] = value
        else:
            setattr(combatant, field, value)


'''
    def update_info(self, data, is_new=False):
        """Update combatant self-serve data properties.

        Code factored out of create_or_update so that when a combatant is
        performing self-serve information update, they cannot change anything
        other than the subset of data (Combatant._combatant_info) they are
        supposed to be able to

        Args:
            data: A dict of combatant data to update
            is_new: Boolean indicating if the combatant record is new or not

        """
        self.validate_data(data)

        # In case something changes
        original_sca_name = self.sca_name
        original_email = self.email

        # Do the updates
        for field, value in data.items():
            if field not in self._combatant_info:
                continue

            # Special cases
            if not is_blank(value):
                if field == "phone":
                    value = re.sub(r"[^0-9]", "", data[field])
                elif field == "dob":
                    # Don't let minors edit their own DOB
                    continue

            if field in self._encrypt_info:
                self.decrypted[field] = value
            else:
                setattr(self, field, value)

        # Combatant changed SCA name
        name_changed = original_sca_name != self.sca_name
        if is_new is False and name_changed and self.accepted_privacy_policy:
            self.card_id = self.generate_card_id()
            emailer = Emailer()
            emailer.send_card_request(self)

        # Log change of email if that is happening
        if original_email != self.email:
            logging.info(
                "changed email address from %s to %s", original_email, self.email
            )

        # return value for CombatantUpdateApi caller
        return self.UpdateInfoReturn(
            sca_name=original_sca_name != self.sca_name,
            email=original_email != self.email,
        )
'''
