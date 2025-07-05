"""
SendCloud API v2/v3 Tracking Schema

Tracking is done via parcel status and tracking URLs
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import json


@dataclass
class TrackingRequest:
    """Simple tracking request - usually just parcel ID or tracking number"""
    parcel_id: Optional[int] = None
    tracking_number: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = {}
        if self.parcel_id is not None:
            result['parcel_id'] = self.parcel_id
        if self.tracking_number is not None:
            result['tracking_number'] = self.tracking_number
        return result


@dataclass
class TrackingEvent:
    """Individual tracking event"""
    timestamp: str
    location: str
    status: str
    details: str


@dataclass
class TrackingData:
    """Tracking information (typically part of parcel response)"""
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    status: Optional[str] = None
    tracking_events: List[TrackingEvent] = field(default_factory=list)
    
    @classmethod
    def from_parcel_response(cls, parcel_data: Dict[str, Any]) -> 'TrackingData':
        """Extract tracking data from parcel response"""
        return cls(
            tracking_number=parcel_data.get('tracking_number'),
            tracking_url=parcel_data.get('tracking_url'),
            status=parcel_data.get('status', {}).get('message') if parcel_data.get('status') else None,
            tracking_events=[]  # SendCloud typically provides tracking via external URL
        )


@dataclass
class TrackingResponse:
    """Tracking response wrapper"""
    tracking_data: TrackingData
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TrackingResponse':
        """Create from dictionary"""
        if 'parcel' in data:
            # This is a parcel response, extract tracking info
            tracking_data = TrackingData.from_parcel_response(data['parcel'])
        else:
            # Direct tracking data
            tracking_data = TrackingData(**data)
        
        return cls(tracking_data=tracking_data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'TrackingResponse':
        """Create from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data) 
