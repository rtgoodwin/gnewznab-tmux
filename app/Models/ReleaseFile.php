<?php

namespace App\Models;

use Blacklight\SphinxSearch;
use Illuminate\Database\Eloquent\Model;

/**
 * App\Models\ReleaseFile.
 *
 * @property int $releases_id FK to releases.id
 * @property string $name
 * @property int $size
 * @property bool $ishashed
 * @property \Carbon\Carbon|null $created_at
 * @property \Carbon\Carbon|null $updated_at
 * @property bool $passworded
 * @property-read \App\Models\Release $release
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Models\ReleaseFile whereCreatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Models\ReleaseFile whereIshashed($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Models\ReleaseFile whereName($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Models\ReleaseFile wherePassworded($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Models\ReleaseFile whereReleasesId($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Models\ReleaseFile whereSize($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Models\ReleaseFile whereUpdatedAt($value)
 * @mixin \Eloquent
 */
class ReleaseFile extends Model
{
    /**
     * @var bool
     */
    protected $dateFormat = false;

    /**
     * @var array
     */
    protected $guarded = [];

    /**
     * @var string
     */
    protected $primaryKey = 'releases_id';

    public function release()
    {
        return $this->belongsTo(Release::class, 'releases_id');
    }

    /**
     * Get releasefiles row by id.
     *
     *
     * @param $id
     * @return \Illuminate\Database\Eloquent\Collection|static[]
     */
    public static function getReleaseFiles($id)
    {
        return self::query()->where('releases_id', $id)->orderBy('name')->get();
    }

    /**
     * @param $guid
     * @return \Illuminate\Database\Eloquent\Collection|static[]
     */
    public static function getByGuid($guid)
    {
        return self::query()
            ->join('releases', 'releases.id', '=', 'release_files.releases_id')
            ->where('releases.guid', $guid)
            ->orderBy('release_files.name')->get();
    }

    /**
     * Delete a releasefiles row.
     *
     *
     * @param $id
     * @return mixed
     * @throws \Exception
     */
    public static function deleteReleaseFiles($id)
    {
        $res = self::query()->where('releases_id', $id)->delete();
        (new SphinxSearch())->updateRelease($id);

        return $res;
    }

    /**
     * Add new files for a release ID.
     *
     *
     * @param        $id
     * @param        $name
     * @param string $hash
     * @param        $size
     * @param        $createdTime
     * @param        $hasPassword
     *
     * @return int
     * @throws \Exception
     */
    public static function addReleaseFiles($id, $name, $hash = '', $size, $createdTime, $hasPassword): int
    {
        $duplicateCheck = self::query()->where('releases_id', $id)->where('name', utf8_encode($name))->first();

        if ($duplicateCheck === null) {
            $insert = self::create(
                [
                    'releases_id' => $id,
                    'name' => utf8_encode($name),
                    'size' => $size,
                    'created_at' => $createdTime,
                    'passworded' => $hasPassword,
                ]
            )->id;

            if (\strlen($hash) === 32) {
                ParHash::insertIgnore(['releases_id' => $id, 'hash' => $hash]);
            }
            (new SphinxSearch())->updateRelease($id);
        }

        return $insert ?? 0;
    }
}
