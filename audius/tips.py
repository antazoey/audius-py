from typing import Dict, Optional, Union

from audius.client import API


class Tips(API):
    def get(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        user_id: Optional[str] = None,
        receiver_min_followers: Optional[int] = None,
        receiver_is_verified: Optional[bool] = None,
        current_user_follows: Optional[str] = None,
        unique_by: Optional[str] = None,
    ):
        """
        Get user tips.

        Args:
            offset (int | None): The number of items to skip. Useful for pagination.
              Defaults to ``None``.
            limit (int | None): The number of items to fetch. Defaults to ``None``.
            user_id (str | None): The user ID of the user making the request. Defaults
              to ``None``.
            receiver_min_followers (int | None): Only include tips from recipients who
              have this many followers. Defaults to ``None``.
            receiver_is_verified (bool | None): Only include tips to recipients that are
              verified. Defaults to ``None``.
            current_user_follows (str | None): Only include tips involving the user's followers
              in the given capacity. Requires ``user_id`` to be set. Defaults to ``None``.
            unique_by (str | None): Only include the most recent tip for a user who was
              involved in the given capacity.
        """

        params: Dict[str, Union[int, str, bool]] = {}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if user_id is not None:
            params["user_id"] = self._handle_id(user_id)
        if receiver_min_followers is not None:
            params["receiver_min_followers"] = receiver_min_followers
        if receiver_is_verified is not None:
            params["receiver_is_verifed"] = receiver_is_verified
        if current_user_follows is not None:
            params["current_user_follows"] = current_user_follows
        if unique_by is not None:
            params["unique_by"] = unique_by

        result = self.client.get("tips", params=params)
        return result.get("data", {})
